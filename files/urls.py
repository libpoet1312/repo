from files.views import *
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # AUTH VIEWS #
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
    ##############

    # CRUD VIEWS #
    path(r'files/myfiles/', Myfiles, name='my_files'),  # LIST MY FILES

    path('files/<slug:slug>/', FileDetailView.as_view(), name='file_detail'),  # FILE DETAIL VIEW

    path(r'files/<area>/', ListView, name='list_files'),  # LIST FILES BY AREA
    path(r'files/<category>/', ListView, name='list_files'),  # LIST FILES BY CATEGORY


    path(r'files/', ListView, name='list_files'),





    path(r'add/', AddFile, name='file_add'),
    ##############

    # AJAX VIEWS #
    path(r'cat/', get_cat_tree_ajax, name='cat_ajax_tree'),
    path(r'area/', get_area_tree_ajax, name='area_ajax_tree'),
    ##############

    path('category/', FileCategoryListView.as_view(), name='category_list'),


    # OTHER VIEWS #
    path(r'tags/', include('taggit_templatetags2.urls')),
    ###############
]
