import os
from django.shortcuts import render
from django.views.generic import *
from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView
from .forms import *
from .models import *
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
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

class FileCreateView(CreateView):
    model = File
    form_class = FileForm
    template_name = 'files/file_add.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.uploader = self.request.user
        return super(FileCreateView, self).form_valid(form)


class TagView(ListView):
    model = File


def ListView(request, area=''):
    files = File.objects.all()
    if request.is_ajax():
        print('AJAX')

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

        print(files)

        html = render_to_string('files/renderlist.html', {'file_list': files})
        return JsonResponse(html, safe=False)
    else:
        print(area)
        string_utf = area.encode()
        print(string_utf)

        return render(request, "files/file_list.html", {
            'file_list': files,
        })


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


def load_first_category(request):
    category = request.GET.get('firstlevel')
    firstlevel = Category.objects.all().filter(level=0)
    print(firstlevel)

    return 0


class FileCategoryListView(View):
    template_name = "movies/movie_category_list.html"

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


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


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
