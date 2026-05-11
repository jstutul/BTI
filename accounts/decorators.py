from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect


def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # 🟡 If not logged in → redirect with type
            if not request.user.is_authenticated:
                role = allowed_roles[0] if allowed_roles else 'student'
                return redirect(f"/accounts/login/?type={role}")

            user_role = getattr(getattr(request.user, 'profile', None), 'role', None)

            if user_role not in allowed_roles:
                return HttpResponseForbidden("You are not allowed to access this page")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator