from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .form import CustomUserCreationForm,CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserNew
    list_display = ['username', 'is_table',]
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('is_table',)}),
    )

admin.site.register(MUser)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(UserNew, CustomUserAdmin)