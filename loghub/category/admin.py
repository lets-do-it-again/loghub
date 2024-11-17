from django.contrib import admin
from .models import Category, Template, UserAccessCategory, Keyword

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description',)
    list_filter = ('parent',)

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('category', 'title')
    search_fields = ('title',)
    autocomplete_fields = ('category',)

class UserAccessCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'role_type')
    list_filter = ('role_type',)
    autocomplete_fields = ('user', 'categories', 'include_categories', 'exclude_categories')

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'value')
    list_filter = ('created_date',)
    autocomplete_fields = ('user_access_category',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(UserAccessCategory, UserAccessCategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)
