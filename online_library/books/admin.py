from django.contrib import admin
from .models import Book,Genre
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.decorators import action, display, register
from django.contrib.admin.sites import AdminSite, site
from django.utils.module_loading import autodiscover_modules
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.decorators import action, display, register
from django.contrib.admin.sites import AdminSite, site
from django.utils.module_loading import autodiscover_modules
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')  # Adjust fields as per your model
    search_fields = ('title', 'author')  # Optional: Add search functionality

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    list_editable = ('description',)
    actions = ['mark_as_featured']
    list_per_page = 20
    list_display_links = ('name',)      