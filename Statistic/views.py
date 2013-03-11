import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Insurance.models import Payment, Accident
from Pasargad.helper import group_required, get_user_name, get_security, Admin
from Statistic.forms import general_form, user__form, owner__form
from Statistic.utils import get_count_report, get_payment_report


@login_required
@group_required(Admin)
def home(request):
    return render(request, 'Statistics/home.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
    })


@login_required
@group_required(Admin)
def general_payments(request):
    chart = None
    if request.method.upper() == 'GET':
        form = general_form()
    else:
        form = general_form(request.POST)
        if form.is_valid():
            report = get_payment_report(Payment.objects.all(), form)
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            title = "Total Income And Expenditure Of {} From {} To {}".format('Pasargad Insurance', from_date, to_date)
            chart = [{"series": [{"stacking": False, "data": report[1], "type": "line", "name": "Expenditure"},
                                 {"stacking": False, "data": report[2], "type": "line", "name": "Income"}],
                      "yAxis": [{"title": {"text": "Income & Expenditure "}}], "chart": {"renderTo": "chart"},
                      "xAxis": [{"categories": report[0], "title": {"text": "Dates"}}],
                      "title": {"text": title}}]
            chart = json.dumps(chart)

    return render(request, 'Statistics/general.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'chart': chart,
    })


@login_required
@group_required(Admin)
def user_payments(request):
    chart = None
    if request.method.upper() == 'GET':
        form = user__form()
    else:
        form = user__form(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            report = get_payment_report(Payment.objects.all().filter(dealer=user), form)
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            title = "Total Income And Expenditure Of {} From {} To {}".format(user, from_date, to_date)
            chart = [{"series": [{"stacking": False, "data": report[1], "type": "line", "name": "Expenditure"},
                                 {"stacking": False, "data": report[2], "type": "line", "name": "Income"}],
                      "yAxis": [{"title": {"text": "Expenditure & Income"}}], "chart": {"renderTo": "chart"},
                      "xAxis": [{"categories": report[0], "title": {"text": "Dates"}}],
                      "title": {"text": title}}]
            chart = json.dumps(chart)

    return render(request, 'Statistics/user.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'chart': chart,
    })


@login_required
@group_required(Admin)
def accidents(request):
    chart = None
    if request.method.upper() == 'GET':
        form = general_form()
    else:
        form = general_form(request.POST)
        if form.is_valid():
            report = get_count_report(Accident.objects.all(), form)
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            title = "Total Accident From {} To {}".format(from_date, to_date)
            chart = [{"series": [{"stacking": False, "data": report[1], "type": "line", "name": "Expenditure"}],
                      "yAxis": [{"title": {"text": "Count"}}], "chart": {"renderTo": "chart"},
                      "xAxis": [{"categories": report[0], "title": {"text": "Dates"}}],
                      "title": {"text": title}}]
            chart = json.dumps(chart)

    return render(request, 'Statistics/accident.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'chart': chart,
    })


@login_required
@group_required(Admin)
def owner_payments(request):
    chart = None
    if request.method.upper() == 'GET':
        form = owner__form()
    else:
        form = owner__form(request.POST)
        if form.is_valid():
            owner = form.cleaned_data['owner']
            report = get_payment_report(Payment.objects.all().filter(owner=owner), form)
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            title = "Total Income And Expenditure Of {} From {} To {}".format(owner, from_date, to_date)
            chart = [{"series": [{"stacking": False, "data": report[1], "type": "line", "name": "Expenditure"},
                                 {"stacking": False, "data": report[2], "type": "line", "name": "Income"}],
                      "yAxis": [{"title": {"text": "Expenditure & Income"}}], "chart": {"renderTo": "chart"},
                      "xAxis": [{"categories": report[0], "title": {"text": "Dates"}}],
                      "title": {"text": title}}]
            chart = json.dumps(chart)

    return render(request, 'Statistics/owner.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'chart': chart,
    })


@login_required
@group_required(Admin)
def contracts(request):
    pass


@login_required
@group_required(Admin)
def attachments(request):
    pass



