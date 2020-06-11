from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegisterForm, ImageForm, CategoryForm, SettingsForm
from .models import Image, Category, Settings
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
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1'] 
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        settings = Settings(user=user, display_width=320, display_height=180)
        settings.save()
        
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
        request.session["msg"] = "New category created."
    else:
        request.session["msg"] = "Error creating category."


    return redirect('all_categories')


@login_required
def all_images(request):
    upload_form = ImageForm()
    images = Image.objects.filter(owner=request.user)
    settings = Settings.objects.filter(user=request.user)[0]

    context = {
        'images': images, 
        'upload_form': upload_form, 
        'display_width': settings.display_width, 
        'display_height': settings.display_height
    }

    return render(request, 'gal/all_images.html', context)


@login_required
def all_categories(request):
    msg = ''

    if "msg" in request.session:
            msg = request.session["msg"]
            del request.session["msg"]

    category_form = CategoryForm()
    categories = Category.objects.filter(owner=request.user)

    return render(request, 'gal/all_categories.html', {'categories': categories, 'category_form': category_form, 'msg': msg})


@login_required
def settings(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            settings = Settings.objects.filter(user=request.user)[0] # OneToOneField created on user registration => there will always be one object
            settings.display_height = form.cleaned_data['new_height']
            settings.display_width = form.cleaned_data['new_width']
            settings.save()
            request.session["msg"] = "Changes saved successfully."
            request.session["alert"] = "success"
        else:
            request.session["msg"] = "Incorrect dimensions (min. 100 max. 500)."
            request.session["alert"] = "warning"
        return redirect('settings')
    else:
        msg = ''
        alert = ''
        if "msg" in request.session and "alert" in request.session:
            msg = request.session["msg"]
            alert = request.session["alert"]
            del request.session["msg"]
            del request.session["alert"]

        settings = Settings.objects.filter(user=request.user)[0] 
        form = SettingsForm(initial={'new_height': settings.display_height, 'new_width': settings.display_width})
        return render(request, 'gal/settings.html', {'form': form, 'msg': msg, 'alert_type': alert})

@require_POST
@login_required
def delete_category(request):
    
    deleted_id = request.POST["cat_id"]
    match = Category.objects.filter(owner=request.user, id=deleted_id)
    
    if len(match):
        match[0].delete()
        request.session["msg"] = 'Category deleted.'
    else:
        request.session["msg"] = 'Incorrect data.'

    return redirect('all_categories')

@login_required
def category(request):
    cat_id = request.GET.get('id', None)

    if cat_id is None:
        return redirect('all_categories')
    else:
        match = Category.objects.filter(owner=request.user, id=cat_id)

        if not len(match):
            return redirect('all_categories')
        else:
            category = match[0]
            images = Image.objects.filter(category=category)
            settings = Settings.objects.filter(user=request.user)[0]

            return render(request, 'gal/category.html', {'category': category, 'images': images, 'display_width': settings.display_width, 'display_height': settings.display_height})