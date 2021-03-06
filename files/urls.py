from taggit_templatetags2.views import TagCanvasListView

from files.views import *
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
import django_cas_ng.views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('info/', InfoView.as_view(), name='info'),
    path('terms/', TermsView.as_view(), name='terms'),

    # AUTH VIEWS #
    path('login/', CustomLoginView.as_view(), name='login'),
    path('caslogin', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path(r'logout/', LogoutView.as_view(), name='cas_ng_logout'),
    ##############
    path(r'files/myfiles/', Myfiles, name='my_files'),  # LIST MY FILES
    path(r'files/myfiles/<pk>/delete', FileDeleteView.as_view(), name='file_delete'),  # DELETE A FILE

    path(r'files/<area>/', ListView, name='list_files'),  # LIST FILES BY AREA
    # path(r'files/<category>/', ListView, name='list_files'),  # LIST FILES BY CATEGORY


    # CRUD VIEWS #
    path('files/file/<slug:slug>/', FileDetailView.as_view(), name='file_detail'),  # FILE DETAIL VIEW






    path(r'files/', ListView, name='list_files'),





    path(r'add/', AddFile, name='file_add'),
    path(r'files/file/<slug:slug>/edit/', AddFile, name='file_edit'),
    ##############

    # AJAX VIEWS #
    path(r'cat/', get_cat_tree_ajax, name='cat_ajax_tree'),
    path(r'area/', get_area_tree_ajax, name='area_ajax_tree'),
    ##############

    path('category/', FileCategoryListView.as_view(), name='category_list'),


    # OTHER VIEWS #
    path(r'tags/', include('taggit_templatetags2.urls')),
    path(r'<tag_id>&<tag_slug>/', ListView, name='myurlname'),



    ###############
]
