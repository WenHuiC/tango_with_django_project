from django.contrib import admin

# Register your models here.
# Category and Page are missing in the admin interface
from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

# Add to interface
# Add further classes by using the admin.site.register() method
# Update the registration to include this customised interface
# from (Category) --> (Category, CategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)

