from files.views import *
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path(r'logout/', LogoutView.as_view(), name='logout'),

    path(r'cat/', get_cat_tree_ajax, name='cat_ajax_tree'),
    path(r'area/', get_area_tree_ajax, name='area_ajax_tree'),



    path(r'list/', ListView, name='list_files'),
    path(r'list/<area>/', ListView, name='list_files'),




    path('<slug:slug>/', FileDetailView.as_view(), name='file_detail'),
    path(r'tags/', include('taggit_templatetags2.urls')),

]