from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib.auth import get_user_model

# Register your models here.

User = get_user_model()  # or from .models import User
admin.site.site_header = "Πίνακας ελέγχου Αποθετηρίου"
admin.site.site_title = "My Product Inventory "


class CategoryAdmin(DjangoMpttAdmin):
    pass


class AreaAdmin(DjangoMpttAdmin):
    pass


class UserAdmin1(UserAdmin):
    list_filter = ('sku', 'unit')


class FileAdmin():

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.id == request.user.id)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Area, AreaAdmin)

admin.site.register(File)
