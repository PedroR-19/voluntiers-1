from django.contrib import admin

from .models import Category, Task


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'profile']
    list_display_links = 'title', 'created_at',
    search_fields = 'id', 'title', 'description', 'slug', 'steps',
    list_filter = 'category', 'profile', 'is_published', \
        'steps_is_html',
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }


admin.site.register(Category, CategoryAdmin)
