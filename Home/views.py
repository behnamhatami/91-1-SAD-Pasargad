from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from Pasargad.helper import *


def home(request):
    error_message = ''

    if not request.user.is_authenticated():
        if request.method.upper() == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is None:
                error_message = 'The username or password you entered is incorrect.'
            elif not user.is_active:
                error_message = 'The user has been disabled by admin.'

            if error_message != '':
                return render(request, 'Home/Signin.html', {
                    'error_message': error_message,
                })
            login(request, user)
            if request.GET.__contains__("next"):
                return redirect(request.GET.get("next"))
            else:
                return redirect('Home:home')
        else:
            return render(request, 'Home/Signin.html')
    else:
        print(get_user_name(request))
        return render(request, 'Home/home.html', {
            'user_name': get_user_name(request),
            'security': get_security(request)
        })