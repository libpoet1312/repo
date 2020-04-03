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


# Create your views here.
class HomeView(TemplateView):
    template_name = 'files/home.html'


def ListView(request):
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
        print(files)

        html = render_to_string('files/renderlist.html', {'file_list': files})
        return JsonResponse(html, safe=False)


    else:
        return render(request, "files/file_list.html", {
            'file_list': files,
        })


## CATEGORY TREE
def get_cat_tree_ajax(request):
    if request.is_ajax():
        tree_set = Category._tree_manager.values()
        data = []
        for i in tree_set:
            if not i['parent_id']:
                parent_id = '#'
            else:
                parent_id = 'j1_' + str(i['parent_id'])
            data.append(
                {"id": 'j1_' + str(i['id']), "parent": parent_id, "text": i['name']}
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
                {"id": 'j1_' + str(i['id']), "parent": parent_id, "text": i['name']}
            )
        # print(json.dumps(data))
        return JsonResponse(json.dumps(data), safe=False)


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