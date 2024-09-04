from django.http import HttpResponseForbidden
from functools import wraps
from .models import User_TypeUser, TypeUser
from django.shortcuts import redirect

def client_required(view_func):
    @wraps(view_func)
    def _wrapper_view(request, *args, **kwargs):
        user = request.user
        client = TypeUser.objects.get(type='Cliente')
        is_client = User_TypeUser.objects.filter(user=user,type_user=client).exists()
        if not is_client:
            print('Acceso solo para los clientes.')
            return redirect('account:Dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapper_view

def is_admin(view_func):
    @wraps(view_func)
    def _wrapper_view(request, *args, **kwargs):
        user = request.user
        #employed = TypeUser.objects.get(type='Empleado')
        #is_employed = User_TypeUser.objects.filter(user=user,type_user=employed).exists()
        is_admin = user.is_staff
        if not is_admin:
            print('Acceso solo para Administración.')
            last_url = request.session.get('last_url','/')
            return redirect('account:Profile')
        return view_func(request, *args, **kwargs)
    return _wrapper_view
