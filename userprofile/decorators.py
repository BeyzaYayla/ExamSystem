from django.http import HttpResponse
from django.shortcuts import redirect

# controls if the user is not authenticated
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontpage')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

# allowed user control for specific functions
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponse('You are not authorised to view this page')

        return wrapper_func

    return decorator

