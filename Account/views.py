from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from Account.forms import *
from Pasargad.helper import *

@login_required
def home(request):
    return render(request, 'Account/home.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
    })


@login_required
def my_logout(request):
    logout(request)
    return redirect('Home:home')


@login_required
def view_profile(request):
    return render(request, 'Account/view_profile.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'property_list': get_property_list(request.user, show_user_form(), id=request.user.id),
    })


@login_required
def change_password(request):
    form = None
    success_message = ''
    if request.method.upper() == 'POST':
        form = Change_password_form(request.user, request.POST)
        if form.is_valid():
            form.save(commit=True)
            success_message = "Password changed successfully."
    else:
        form = Change_password_form(request.user)

    return render(request, 'Account/change_password.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'success_message': success_message,
    })


@login_required
def edit_profile(request):
    form = None
    success_message = ''

    if request.method.upper() == 'POST':
        form = edit_user_form(request.user, request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            success_message = 'Changes Done.'
    else:
        form = edit_user_form(request.user, instance=request.user)

    return render(request, 'Account/edit_profile.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Admin)
def change_user_password(request):
    form = None
    success_message = ''

    if request.method.upper() == 'POST':
        form = Change_user_password_form(request.user, request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Password for user name "' + form.cleaned_data[
                'username'] + '" has been changed successfully.'
    else:
        form = Change_user_password_form(request.user)

    return render(request, 'Account/change_user_password.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Admin)
def create_user(request):
    success_message = ''
    form = None

    if request.method.upper() == 'POST':
        form = Create_user_form(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'User name "' + form.cleaned_data['username'] + '" created successfully.'
    else:
        form = Create_user_form()

    return render(request, 'Account/create_user.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Admin)
def delete_user(request):
    form = None
    success_message = ''
    if request.method.upper() == 'POST':
        form = Delete_user_form(request.user, request.POST)
        if form.is_valid():
            form.save()
            success_message = 'User name "' + form.cleaned_data['username'] + '" Deleted successfully.'
    else:
        form = Delete_user_form(request.user)

    return render(request, 'Account/delete_user.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'success_message': success_message,
    })
