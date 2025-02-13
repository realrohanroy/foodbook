from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Recipe, Review
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from .forms import RecipeForm, ReviewForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required  # Ensure that only logged-in users can create a recipe
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)  # Create the recipe instance but don't save it yet
            recipe.user = request.user  # Associate the recipe with the logged-in user
            print(f":User     {recipe.user}") 
            recipe.save()  # Now save the recipe
            return redirect('index')  # Redirect to a success page or the index
    else:
        form = RecipeForm()
    return render(request, 'TestApp/create_recipe.html', {'form': form})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = recipe.reviews.all()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        review_form = ReviewForm()
    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form,
    })

def index(request):
    recipes = Recipe.objects.all()  # Fetch all recipes
    return render(request, 'TestApp/index.html', {'recipes': recipes})

def about(request):
    return render(request, 'TestApp/about.html')

def projects(request):
    return render(request, 'TestApp/projects.html')

# User login view
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the home page
            else:
                form.add_error(None, "Invalid email or password.")  # Add error message
    else:
        form = UserLoginForm()
    return render(request, 'TestApp/login.html', {'form': form})

# Contact form view
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success') 
    else:
        form = ContactForm() 
    return render(request, 'TestApp/contact.html', {'form': form})   

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user,  backend='django.contrib.auth.backends.ModelBackend') # Automatically log in the user after registration
            return redirect('index')  # Redirect to the home page
    else:
        form = UserRegistrationForm()
    return render(request, 'TestApp/register.html', {'form': form})

# User account view
@login_required
def myaccount(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  # Save the user instance, including the profile picture and cropping info
            return redirect('myaccount')  # Redirect to the same page after saving
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'TestApp/myaccount.html', {'form': form})

# Logout view
def logout_view(request):
    if request.method == 'POST':
        logout(request)  # Log the user out
        return redirect('index')  # Redirect to your app's home page
    return HttpResponseForbidden()  # Return a 403 Forbidden response for other methods