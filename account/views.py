from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .middleware import catchLogin404Middleware
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm, PermissionForm, TypeUserForm
from django.contrib import messages

from notificaciones.models import Notification

from django.utils.decorators import decorator_from_middleware

from .models import Profile, TypeUser, User_TypeUser
from .permissions import client_required,is_admin


catch_login_404 = decorator_from_middleware(catchLogin404Middleware)

@catch_login_404
def Login(request):
    user = request.user
    if isinstance(user, User):
        last_url = request.session.get('last_url','/')
        return redirect(last_url)
    if request.method == 'POST':        
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']            
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                if user.is_staff:
                    return redirect('account:Dashboard')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('account:Profile')  
    else:
        form = LoginForm()                      
    return render(request,'auth/login.html',{'form':form})

def Logout(request):
    logout(request)
    return redirect('account:Login')


def Register(request):
    
    if(request.user.is_authenticated):
        last_url = request.session.get('last_url','/')
        return redirect(last_url)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        #print(form.errors.as_data())        
        if form.is_valid():
            new_user = form.save()            
            Profile.objects.create(user=new_user)
            type_user = TypeUser.objects.get(type='Cliente')
            user_client = User_TypeUser(user=new_user,type_user=type_user)
            user_client.save()
            messages.success(request, 'Registration successful.')
            return redirect('account:Login')        
    else:
        form = RegisterForm()
    return render(request,'auth/register.html',{'form':form})

@login_required(login_url='account:Login')
@is_admin
def Dashboard(request):    
    if request.method == 'POST':        
        if 'form-type-user' in request.POST:
            typeUserForm = TypeUserForm(request.POST)
            if typeUserForm.is_valid():            
                new_type_user = typeUserForm.save()                
                messages.success(request, f'Type user {new_type_user.type} created.')
                return redirect('account:Dashboard')
        elif 'form-permission' in request.POST:
            permissionForm = PermissionForm(request.POST)          
            if permissionForm.is_valid():
                print('Datos completos')
        permissionForm = PermissionForm()
        typeUserForm = TypeUserForm()
    else:
        typeUserForm = TypeUserForm()
        permissionForm = PermissionForm()
    return render(request,'auth/dashboard.html',{
        'permissionForm':permissionForm,
        'typeUserForm':typeUserForm
        })

def CreateTypeUser(request):
    if request.method == 'POST':
        typeUserForm = TypeUserForm(request.POST)
        print(typeUserForm)
        if typeUserForm.is_valid():
            typeUserForm.save()
    else:
        typeUserForm = TypeUserForm()
    return redirect('account:Dashboard')





@login_required(login_url='account:Login')
def ProfileView(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    return render(request,'cliente/profile.html',{'profile':profile})

def EditProfile(request):
    pass