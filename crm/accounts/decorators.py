from django.http import HttpResponse
from django.http import request
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator (view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None
            if request.user.groups.exists(): #here, users.groups is referring to the group assigned to the logged in user, since this decorator runs after the user has logged in, so it can access its variables
                group = request.user.groups.all()[0].name #retrieves all the groups of the logged in user and checks if the first group falls under the permitted group list
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request,*args, **kwargs)
    
    return wrapper_function