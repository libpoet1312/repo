import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import *
from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView
from .forms import *
from .models import *
from django.urls import reverse_lazy
import json
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.db.models import Q
from django.shortcuts import get_object_or_404


# Create your views here.
class HomeView(TemplateView):
    template_name = 'files/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_files'] = File.objects.all().count()
        context['categories'] = Category.objects.all()
        context['areas'] = Area.objects.all().filter(level=0)
        return context


class FileDetailView(DetailView):
    model = File


@login_required
class FileCreateView(CreateView):
    model = File
    form_class = FileForm
    template_name = 'files/file_add.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.uploader = self.request.user
        return super(FileCreateView, self).form_valid(form)


def filter(request, files):
    text_search = request.GET.get('text_search')
    if text_search:
        files = files.filter(
            Q(name__contains=text_search) |
            Q(summary__contains=text_search)
        )

    tags = request.GET.getlist('tags')
    if tags:
        files = files.filter(tags__name__in=tags).distinct()

    categories = request.GET.getlist('categories')
    if categories:
        cat_path = []
        cat_obj = []
        query = []
        cat = Category.objects.all()
        for c in cat:
            cat_obj.append(c)
            cat_path.append(c.get_category_greek())

        print(cat_obj)

        for category in categories:
            print('category=' + category)
            if category in cat_path:
                index = cat_path.index(category)
                print(cat_obj[index])
                query.append(cat_obj[index])
        files = files.filter(category__in=query)

    areas = request.GET.getlist('areas')

    if areas:
        q = []
        q1 = []
        print('ORIGINAL AREAS', areas)
        for idx, area in enumerate(areas):
            print(area)
            if '/' in area:
                n = area.split('/')
                areas[idx] = n[1]
            else:
                area_obj = get_object_or_404(Area, name=area)
                area_obj_descendants = area_obj.get_descendants(include_self=True)
                for child in area_obj_descendants:
                    q.append(child)

            print('NEW AREAS=', areas)
            print('Q=', q)

        files = files.filter(
            Q(area__name__in=areas) |
            Q(area__name__in=q)
        ).distinct()

    return files


@login_required()
def Myfiles(request):
    print('MY FILES')
    files = File.objects.all().order_by('dateCreated')
    page = 1
    files = files.filter(uploader__username__exact=request.user)
    if request.is_ajax():
        pageres = request.GET.get('page')
        if pageres is not None:
            page = pageres

        files = filter(request, files)

        paginator = Paginator(files, 3)

        try:
            file_list = paginator.page(page)
        except PageNotAnInteger:
            file_list = paginator.page(1)
        except EmptyPage:
            file_list = paginator.page(paginator.num_pages)

        html = render_to_string('files/renderlist.html', {'file_list': file_list})
        return JsonResponse(html, safe=False)
    else:
        return render(request, "files/file_list.html", {})


def ListView(request, area='', category=''):
    print('LIST VIEW')
    files = File.objects.all().order_by('dateCreated')
    page = 1
    print(request.user.is_authenticated)
    # if request.user.is_authenticated:
    #    files = files.filter(uploader__username__exact=request.user)

    if request.is_ajax():
        pageres = request.GET.get('page')
        if pageres is not None:
            page = pageres

        files = filter(request, files)

        print(files)
        paginator = Paginator(files, 3)

        try:
            file_list = paginator.page(page)
        except PageNotAnInteger:
            file_list = paginator.page(1)
        except EmptyPage:
            file_list = paginator.page(paginator.num_pages)

        html = render_to_string('files/renderlist.html', {'file_list': file_list})
        return JsonResponse(html, safe=False)

    else:

        return render(request, "files/file_list.html", {})


## CATEGORY TREE
def get_cat_tree_ajax(request):
    if request.is_ajax():
        tree_set = Category._tree_manager.values()
        # print(tree_set)
        data = []
        for i in tree_set:
            if not i['parent_id']:
                parent_id = '#'
            else:
                parent_id = 'j1_' + str(i['parent_id'])
            data.append(
                {"id": 'j1_' + str(i['id']), "parent": parent_id, "text": i['name'], "slug": i['slug']}
            )
        # print(json.dumps(data))
        return JsonResponse(json.dumps(data), safe=False)
        # return HttpResponse(json.dumps(data), content_type="application/json")


## GET AREA TREE
def get_area_tree_ajax(request):
    if request.is_ajax():
        tree_set = Area._tree_manager.values()
        data = []
        for i in tree_set:
            if not i['parent_id']:
                parent_id = '#'
            else:
                parent_id = 'j1_' + str(i['parent_id'])
            data.append(
                {"id": 'j1_' + str(i['id']), "parent": parent_id, "text": i['name'], "slug": i['slug']}
            )
        # print(json.dumps(data))
        return JsonResponse(json.dumps(data), safe=False)


class FileCategoryListView(View):
    template_name = "files/category_list.html"

    def get(self, request, *args, **kwargs):
        context = {
            "categories": Category.objects.all(),
        }
        return render(request, self.template_name, context)


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'files/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('home')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'files/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('home')


@login_required
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('DELETE')

    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@login_required
@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


def load_first_category(request):
    if request.is_ajax():
        cat = request.GET.get('category2')
        skata = request.GET.get('skata')
        print('cat = ', cat)
        print('skata = ', skata)

        data = Category.objects.all().filter(name=cat)

        print(data)

        return JsonResponse(json.dumps(data), safe=False)




@login_required
def AddFile(request, slug):



    proptypiako = Category.objects.get(name='Προπτυχιακό').get_children()
    prop = [str(p) for p in proptypiako]

    metaptyxiako = Category.objects.get(name='Μεταπτυχιακό').get_children()
    meta = [str(m) for m in metaptyxiako]

    if request.method == 'GET':
        if request.is_ajax():
            cat1 = request.GET.get('cat1')
            if cat1:
                c = cat1.split('/')
                obj = get_object_or_404(Category, name=c[1])
                print(obj)
                obj_descendants = obj.get_children()
                print(obj_descendants)
                res = [str(m) for m in obj_descendants]

                return JsonResponse(json.dumps(res), safe=False)

            return JsonResponse('dsad', safe=False)

        else:
            if slug:
                print('edit')
                file = get_object_or_404(File, slug=slug)
                form = FileForm(request.POST or None, instance=file)
                print(form.initial)
            else:
                form = FileForm()
            return render(request, 'files/file_add.html', {'form': form, 'prop': prop, 'meta': meta})
    else:
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            # process the data in form.cleaned_data as required

            obj = form.save(commit=False)

            # find category
            cat1 = request.POST.get('cat1')

            if cat1:
                obj.uploader = request.user

                c = cat1.split('/')
                # print(c)
                parent = get_object_or_404(Category, name=c[0])

                o = Category.objects.all().get(Q(name=c[1]) & Q(parent=parent))
                print('O=', o)

                # set category
                cat2 = request.POST.get('cat2')
                if cat2:
                    # if category = μαθημα
                    # print(cat2)
                    o = Category.objects.all().get(name=cat2)

                obj.category = o

                obj.save()

                form.save_m2m()

                return redirect('file_detail', slug=obj.slug)

            else:
                return render(request, 'files/file_add.html', {'form': form, 'prop': prop, 'meta': meta})

        else:

            cat1 = request.POST.get('cat1')
            print(cat1)

            return render(request, 'files/file_add.html', {'form': form, 'prop': prop, 'meta': meta})
