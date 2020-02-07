from django.contrib import admin

# Register your models here.
# Category and Page are missing in the admin interface
from django.contrib import admin
from rango.models import Category, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Add to interface
# Add further classes by using the admin.site.register() method
admin.site.register(Category)
admin.site.register(Page, PageAdmin)
