import json

from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from main.functions import get_current_role
# from mechion_test.settings import CUSTOMER_LOGIN_URL



def role_required(roles):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            current_role = get_current_role(request)
            if not current_role in roles:
                if request.is_ajax():
                    response_data = {
                        "status": "false",
                        "stable": "true",
                        "title": "Permission Denied",
                        "message": "You have no permission to do this action."
                    }
                    return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                else:
                    context = {
                        "title": "Permission Denied"
                    }
                    return render(request, 'errors/403.html', context)

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


# from django.shortcuts import redirect
# from functools import wraps

# def web_login_required(function=None, session_key='user'):
#     def decorator(view_func):
#         @wraps(view_func)
#         def f(request, *args, **kwargs):
#             if session_key in request.session:
#                 return view_func(request, *args, **kwargs)
#             return redirect(reverse(CUSTOMER_LOGIN_URL))
#         return f
#     if function is not None:
#         return decorator(function)
#     return decorator
