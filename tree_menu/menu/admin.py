from django.contrib import admin
from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu', 'parent', 'named_url', 'custom_url']
    list_filter = ['menu']
    search_fields = ['title', 'named_url', 'custom_url']
