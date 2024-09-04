from typing import Any
from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

from .models import Profile, TypeUser, User_TypeUser

from itertools import groupby #Agrupacion de permisos





class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'username': forms.TextInput(attrs={'required':False})
        }
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].required = False

    def save(self, commit=True):
       user = super().save(commit=False)
       password = self.cleaned_data["password"]
       user.set_password(password)  # Esto se asegura de que la contraseña se hashee
       if commit:
           user.save()
       return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm','Passwords do not match')
        
        return cleaned_data

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            self.add_error('username','Username already exists')
        return username
    
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            self.add_error('email','Email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password',e)
        return password

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput) 
    password = forms.CharField(widget=forms.PasswordInput)      

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is None:
            self.add_error('username','Username does not exist')
        if username == '':
            self.add_error('username','Username is required')
        return username

    def clean_password(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']        
        if password == '':
            self.add_error('password','Password is required')
        else:
            try:
                print(username,password)
                user = authenticate(username=username,password=password)#User.objects.get(username= username)
                #hashed_password = user.password
                #print(hashed_password)
                print(user)
                if not user:#check_password(password,hashed_password):
                    self.add_error('password','Password is incorrect')
            except User.DoesNotExist:
                user = None
        return password

class TypeUserForm(forms.Form):
    type = forms.CharField(widget=forms.TextInput)
    
    def save(self):        
        type_ = self.cleaned_data["type"]
        type_user = TypeUser(type=type_)
        type_user.save()
        return type_user


    def clean_type(self):
        cleaned_data = super().clean()
        type_ = cleaned_data['type']
        if type_ == '':
            self.add_error('type','Type is required')
        return type_



def get_permissions_grouped_by_model():
    permissions = Permission.objects.all().select_related('content_type')
    
    # Agrupar por app_label
    permissions_by_app = {}
    for app_label, perms in groupby(permissions, lambda perm: perm.content_type.app_label):
        permissions_by_app[app_label] = list(perms)

    # Agrupar por model
    permissions_by_model = {}
    for model, perms in groupby(permissions, lambda perm: perm.content_type.model):
        permissions_by_model[model] = list(perms)

    return permissions_by_model

class PermissionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput)
    type_user = forms.ModelChoiceField(queryset=TypeUser.objects.all())
    #permission = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),widget = forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        permissions_by_model = get_permissions_grouped_by_model()
        
        for model, perms in permissions_by_model.items():
            self.fields[f'{model}_permissions'] = forms.ModelMultipleChoiceField(
                queryset=Permission.objects.filter(id__in=[perm.id for perm in perms]),
                widget=forms.CheckboxSelectMultiple,
                label=f'Permisos de {model.capitalize()}'
            )

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name']
        if name == '':
            self.add_error('name','Name is required')
        return name
    
    def clean_type_user(self):
        cleaned_data = super().clean()
        type_user = cleaned_data['type_user']
        if type_user == '':
            self.add_error('type_user','Type user is required')
        return type_user

    def clean_permission(self):
        cleaned_data = super().clean()
        permission = cleaned_data['permission']
        if permission == '':
            self.add_error('permission','Permission is required')
        return permission