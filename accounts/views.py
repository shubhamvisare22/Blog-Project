from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View
from .models import User, UserProfile
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, self.template_name)

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, self.template_name)

    def post(self, request):
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            is_author = request.POST.get('is_author')

            if not User.objects.filter(username=username).exists():
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                )
                user.set_password(password)
                user.save()

                if is_author:
                    UserProfile.objects.create(is_author=True, user=user)
                else:
                    UserProfile.objects.create(is_author=False, user=user)

                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        try:
            logout(request)
            return JsonResponse({'status': 1})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})


@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, self.template_name)
