from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib import messages


class UserDecorators:
    @staticmethod
    def is_authenticated(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = request.user
            if (user.is_authenticated and user.is_active and not user.is_staff or user.is_superuser):
                messages.error(request, 'You do not have access to this page.')
                return redirect("user_profile")
            return view_func(request, *args, **kwargs)
        return wrapper_func

    @staticmethod
    def is_staff_admin_or_superuser(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = request.user
            if (user.is_authenticated and user.is_staff or user.is_superuser):
                messages.error(request, 'You do not have access to this page')
                return HttpResponseRedirect("/admin")
            return view_func(request, *args, **kwargs)
        return wrapper_func
