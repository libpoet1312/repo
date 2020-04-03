from django.contrib import admin
from .models import *
from django_mptt_admin.admin import DjangoMpttAdmin
# Register your models here.


class CategoryAdmin(DjangoMpttAdmin):
    pass


class AreaAdmin(DjangoMpttAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(File)
