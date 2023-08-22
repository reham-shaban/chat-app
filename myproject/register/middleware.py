from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

# check for login
class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path == reverse('auth:login'):
            if not request.path == reverse('auth:register'):
                return redirect(reverse('auth:login'))

        response = self.get_response(request)
        return response
