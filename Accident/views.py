from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from Pasargad.helper import *
from Accident.forms import *


@login_required
@group_required(Secretory, Expert)
def home(request):
    return render(request, 'Accident/home.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
    })


@login_required
@group_required(Secretory)
def create_accident(request):
    if request.method.upper() == 'GET':
        form = accident_form_create()
    else:
        form = accident_form_create(request.POST)
        if form.is_valid():
            accident = form.save()
            return redirect('Accident:view_accident', accident.id)

    return render(request, 'Accident/create_accident.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
    })


@login_required
@group_required(Secretory, Expert)
def view_accident(request, aid):
    accident = get_object_or_404(Accident, pk=aid)
    property_set = [get_property_list(accident, accident_form_show(), id=aid, title='Accident')]

    if accident.get_report() is not None:
        property_set.append(
            get_property_list(accident.get_report(), report_form_show(), id=accident.get_report().id, title='Report'))

    if accident.payment is not None:
        property_set.append(
            get_property_list(accident.payment, payment_form_show(), id=accident.payment.id, title='Payment'))

    return render(request, 'Accident/view_accident.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'accident_id': aid,
        'property_set': property_set,
    })


@login_required
@group_required(Expert)
def finalize_accident(request, aid):
    form = None
    accident = get_object_or_404(Accident, pk=aid)

    if request.method.upper() == 'POST':
        report_instance = Report(date=timezone.now(), accident=accident)
        form = report_form_edit(request.POST, instance=report_instance)
        if form.is_valid():
            form.save()
            payment = Payment(cost=-form.cleaned_data['cost'], date=report_instance.date, dealer=request.user,
                              owner=accident.vehicle.vehicle_owner)
            payment.save()
            accident.payment = payment
            accident.save()
            return redirect('Accident:view_accident', aid=aid)
    else:
        form = report_form_edit()

    return render(request, 'Accident/finalize_accident.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'accident_id': aid,
        'form': form,
    })


@login_required
@group_required(Expert, Secretory)
def accident(request):
    form = None
    if request.method.upper() == 'POST':
        form = search_accident_form(request.POST)
        if form.is_valid():
            return redirect('Accident:view_accident', aid=form.cleaned_data['accident'])
    else:
        form = search_accident_form()

    return render(request, 'Accident/search_accident.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
    })

