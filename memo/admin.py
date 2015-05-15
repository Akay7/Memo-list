from django.contrib import admin
from .models import Memo, Category


class MemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'chosen', 'owner']

admin.site.register(Memo, MemoAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)