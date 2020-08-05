from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django import forms
from .models import Category, File, Area
from mptt.forms import TreeNodeMultipleChoiceField
from django_comments_xtd.forms import XtdCommentForm
from django_comments_xtd.models import TmpXtdComment


class MyCommentForm(XtdCommentForm):

    def get_comment_create_data(self, site_id=None):
        data = super(MyCommentForm, self).get_comment_create_data()
        return data


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class FileForm(forms.ModelForm):
    area = TreeNodeMultipleChoiceField(queryset=Area.objects.all(), label="Επιστημονική Περιοχή",
                                       level_indicator=u'___')

    class Meta:
        model = File
        fields = (
            'name', 'summary', 'tags', 'file', 'thumbnail',
            'author', 'author_email', 'area')


class UpdateFileForm(forms.ModelForm):
    area = TreeNodeMultipleChoiceField(queryset=Area.objects.all(), label="Επιστημονική Περιοχή",
                                       level_indicator=u'___', )
    file = forms.FileField(required=False, )
    thumbnail = forms.ImageField(required=False, )

    class Meta:
        model = File
        fields = (
            'name', 'summary', 'tags', 'file', 'thumbnail',
            'author', 'author_email', 'area',)
