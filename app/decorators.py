from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.http import HttpRequest
from django.shortcuts import redirect
from functools import wraps


def role_required(role_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_anonymous:
                return redirect("main")
            user_role = 'king' if request.user.king is not None else ('subject' if request.user.subject is not None else 'user')

            if user_role == role_name:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper_func
    return decorator