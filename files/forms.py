from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from .models import Category, File, Area
from mptt.forms import TreeNodeChoiceField
from django_select2.forms import ModelSelect2Widget, Select2Widget, Select2TagWidget
from django.db.models import Q


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


def get_query_set():
    data = Category.objects.all().filter(level=1)
    return data


class FileForm(forms.ModelForm):
    area = TreeNodeChoiceField(queryset=Area.objects.all(), label="Επιστημονική Περιοχή", widget=Select2Widget,
                               level_indicator=u'___')
    # category = TreeNodeChoiceField(queryset=Category.objects.all(), label="Κατηγορία", widget=Select2Widget,
    #                                level_indicator=u'')
    #
    # category2 = TreeNodeChoiceField(
    #     queryset=Category.objects.all().filter(Q(level=1) | Q(level=0)),
    #     label=u"category2",
    #     widget=Select2Widget,
    #     level_indicator=u'+--'
    # )
    #
    # course = TreeNodeChoiceField(
    #     required=False,
    #     queryset=Category.objects.all().filter(level=2),
    #     label=u"category3",
    #     level_indicator=u'',
    #     widget=Select2Widget(
    #
    #     )
    # )

    class Meta:
        model = File
        fields = (
            'name', 'summary', 'tags', 'file', 'thumbnail',
            'author',
            'author_email',)
