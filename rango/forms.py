from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Please enter the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    # Defined forms.CharField for the title field
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    # Defined forms.URLField for the url field
    # The max_length=200 identical to the maximum length of each field
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # We don't need every field in the model present.
        # Some fields may allow NULL values; we may not want to include them
        # The foreign keys are hidden here.
        # Can either exclude the category field from the form
        # , or specify the fields to include (Don't include the category field)
        # fields = ('title', 'url', 'views')
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        # use .get() method to obtain the form's value
        # .get return "None" rather than a KeyError exception if value is not entered to the form field
        # (entry will not exist if not entered)
        url = cleaned_data.get('url')

        # If rul is not empty and doesn't start with 'http://', then prepend 'http://'
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data

# chap 9
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)