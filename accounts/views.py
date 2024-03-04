from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
import json
from .models import User, UserProfile


def login_view(request):

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                response = {'status': 1}
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                return JsonResponse({'status': 0}, safe=False)
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)}, safe=False)

    return render(request, 'login.html')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            is_author = request.POST.get('is_author')
            print(f"\n\nis_author ---------------------------> {is_author}")
            if is_author != "on":
                is_author = True
            else:
                is_author = False

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
                return JsonResponse({'status': 1})

            else:
                return JsonResponse({'status': 0})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})

    return render(request, 'register.html')


def logout_view(request):
    if request.method == 'POST':
        try:
            logout(request)
            return JsonResponse({'status': 1})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'profile.html')
