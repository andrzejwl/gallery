from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegisterForm, ImageForm, CategoryForm
from .models import Image, Category
from datetime import datetime

def index(request):
    if request.user.is_authenticated:
        return redirect('panel')
    message = request.session.get("message", None)
    if message is not None: request.session.pop("message")

    register_form = RegisterForm()
    return render(request, 'gal/index.html', {'register_form': register_form, 'message': message})

@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        request.session["message"] = "Account created succesfully." 
    else:
        request.session["message"] = "Data didn't match the requirements specified above."
    return redirect('index')
    


@require_POST
def login(request):
    # TODO: login form
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        dj_login(request, user)
        request.session["username"] = username
        return redirect('panel')
    else:
        request.session["message"] = "Incorrect user data."
        return redirect('index')

@require_POST
@login_required
def logout(request):
    dj_logout(request)
    return redirect('index')

@login_required
def panel(request):
    upload_form = ImageForm(initial={'owner': request.user})
    cat_form = CategoryForm()
    images = Image.objects.filter(owner=request.user)
    categories = Category.objects.filter(owner=request.user)
    
    return render(request, 'gal/panel.html', {'upload_form': upload_form, 'category_form': cat_form, 'images': images, 'categories': categories})

@require_POST
@login_required
def upload(request):
    user = request.user
    form = ImageForm(request.POST, request.FILES)

    if form.is_valid():
        image = Image(
                    owner=request.user, \
                    image=request.FILES['image'], \
                    description=form.cleaned_data['description'],\
                    category=form.cleaned_data['category'],\
                    upload_date=datetime.now()
                )

        image.save()

    return redirect('panel')

@require_POST
@login_required
def create_category(request):
    user = request.user
    form = CategoryForm(request.POST)

    if form.is_valid():
        new_cat = Category(
            owner=user, \
            name=form.cleaned_data['name']
        )

        new_cat.save()
    
    return redirect('panel')


@login_required
def all_images(request):
    upload_form = ImageForm()
    images = Image.objects.filter(owner=request.user)

    return render(request, 'gal/all_images.html', {'images': images, 'upload_form': upload_form})


@login_required
def all_categories(request):
    category_form = CategoryForm()
    categories = Category.objects.filter(owner=request.user)

    return render(request, 'gal/all_categories.html', {'categories': categories, 'category_form': category_form})