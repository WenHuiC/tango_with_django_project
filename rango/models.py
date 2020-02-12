from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    # slug = models.SlugField(blank=True)
    # Solution one : add blank=True to allow the blank entries

    # Chap6 - Add slug field to make readable urls
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    # adding meta class can change the displayed name in admin interface
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

# Why not add these here???
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title