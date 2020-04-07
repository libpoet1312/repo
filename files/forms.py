from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from .models import Category, File, Area
from mptt.forms import TreeNodeChoiceField
from django_select2.forms import ModelSelect2Widget, Select2Widget
from django.forms import Select
from django.utils.html import mark_safe


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class FileForm(forms.ModelForm):

    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     label="Κατηγορία",
    #     widget=ModelSelect2Widget(
    #         model=Category,
    #         search_fields=['name__icontains']
    #     )
    # )
    area = TreeNodeChoiceField(queryset=Area.objects.all(), label="Επιστημονική Περιοχή", widget=Select2Widget,
                                   level_indicator=u'___')
    category = TreeNodeChoiceField(queryset=Category.objects.all(), label="Κατηγορία", widget=Select2Widget, level_indicator=u'')

    class Meta:
        model = File
        fields = ('name', 'summary', 'category','area', 'tags', 'file', 'thumbnail', 'author', 'author_email',)
