from django.shortcuts import render
# make sure the import exist

from django.http import HttpResponse
# import the Category model
from rango.models import Category
# import the Page model
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#  or can add like: from django.contrib.auth import authenticate, login, logout


def index(request):
    #chap 6
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!) 
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list


    # Before Chap 5
    # # Construct a dictionary to pass to the template engine as its context.
    # # Note the key boldmessage matches to {{boldmessage}} in the template!
    # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    
    #Render the response and send it back
    return render(request, 'rango/index.html', context = context_dict)
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")


def about(request):
    # chap 8
    # prints out whether the method is a Get or a Post
    print(request.method)
    # prints out the user name, if no one is logged in it prints 'AnonymousUser'
    print(request.user)
    return render(request, 'rango/about.html', {})


    # context_dict = {'putTutorial' : 'This tutorial has been put together by Wenhui.'}
    
    # return render(request, 'rango/about.html', context = context_dict)
    # # return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine
    context_dict = {}

    try:
        # the .get() method returns one model instance (if exist) or an exception
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages
        # The filter() method will returns a list of page objects or an empty list
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages
        context_dict['pages'] = pages
        # Adds category objects from the database to the context dictionary
        # to verify that the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Render the response and return it to the client via a category.html template
    return render(request, 'rango/category.html', context=context_dict)


    # chapter 7
@login_required    
def add_category(request):
    form = CategoryForm()

        # Chek if the HTTP request is a POST - did the user submit data via the form?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)
            # cat = form.save(commit=True)
            # print(cat, cat.slug)
            # Now that the category is saved, we could confirm this
            # For now, just redirect the user back to the index view
            return redirect('/rango/')
        else:
            # If the supplied form contained errors... 
            print(form.errors) # just print to the terminal

        # Handle the bad form, new form, or no form supplied cases
        # Render the form eith error messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful
    # Set to False initially. Code changes value to 
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProdile instance
            # Since we need to set the user attribute ourselves
            # we set commit=False. This delays saving the model
            # Until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and 
            # put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances
        # These forms will be blank, ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request, 'rango/register.html',
                            context = {'user_form': user_form,
                                        'profile_form': profile_form,
                                        'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user
        # This information is obtained from the login form
        # We use request .POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned id it is
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found
        if user:
            # Is the account active? It could have been disabled
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # An inactive account was used - logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provied. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so desplay the login form.
    # This scenario would most likely be a HTTP GET
    else:
        # No context variables to pass to the template system, hence the 
        # blank dictionary object...
        return render(request, 'rango/login.html')

def some_view(request):
    if not request.user.is_acthenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

@login_required
def restricted(request):
    context_dict = {}
    # return HttpResponse("Since you're logged in, you can see this text!")
    return render(request, 'rango/restricted.html', context=context_dict)

# Use the login_required() decorator to ensure only those logged in can
# access the view
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out
    logout(request)
    # Take the user back to the homepage
    return redirect(reverse('rango:index'))

