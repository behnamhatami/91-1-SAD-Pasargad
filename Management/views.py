from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from Insurance.models import *
from Pasargad.helper import *
from Management.forms import *


@login_required
@group_required(Admin, Secretory, Expert)
def home(request):
    return render(request, 'Management/home.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
    })


@login_required
@group_required(Admin, Secretory, Expert)
def strategy(request):
    queryset = Insurance_type.objects.all()
    form_head = Insurance_type_show_form()
    property_set = []
    for item in queryset:
        property_set.append(get_property_list(item, form_head, id=item.id))
    return render(request, 'Management/strategy.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "There isn't any strategy" if len(property_set) == 0 else '',
    })


@login_required
@group_required(Admin)
def create_strategy(request):
    success_message = None

    if request.method.upper() == 'POST':
        form = Insurance_type_show_form(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Insurance strategy added."
        else:
            pass
    else:
        form = Insurance_type_show_form()

    return render(request, 'Management/create_strategy.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Admin, Secretory, Expert)
def view_strategy(request, stid):
    strategy = get_object_or_404(Insurance_type, pk=stid)
    form = Insurance_type_show_form(instance=strategy)

    return render(request, 'Management/view_strategy.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'strategy_id': stid,
        'property_list': get_property_list(strategy, form, id=strategy.id),
    })


@login_required
@group_required(Admin)
def edit_strategy(request, stid):
    success_message = None
    form = None

    strategy = get_object_or_404(Insurance_type, pk=stid)
    if request.method.upper() == 'POST':
        form = Insurance_type_show_form(request.POST, instance=strategy)
        if form.is_valid():
            form.save()
            success_message = "Changes applied."
    else:
        form = Insurance_type_show_form(instance=strategy)

    return render(request, 'Management/edit_strategy.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'strategy_id': stid,
        'success_message': success_message,
    })


@login_required
@group_required(Admin)
def delete_strategy(request, stid):
    strategy = get_object_or_404(Insurance_type, pk=stid)

    if request.method.upper() == 'POST':
        strategy.delete()
        return redirect('Management:strategy')

    return render(request, 'Management/delete_strategy.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'strategy': strategy,
    })


@login_required
@group_required(Admin, Secretory, Expert)
def plan(request):
    queryset = Insurance_plan.objects.all()
    form_head = Insurance_plan_show_form()
    property_set = []
    for item in queryset:
        property_set.append(get_property_list(item, form_head, item.id))
    return render(request, 'Management/plan.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "There isn't any plan" if len(property_set) == 0 else '',
    })


@login_required
@group_required(Admin)
def create_plan(request):
    success_message = None

    if request.method.upper() == 'POST':
        form = Insurance_plan_show_form(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Insurance plan added."
            for name in form.fields:
                form.fields[name].widget.attrs['readonly'] = True
        else:
            pass
    else:
        form = Insurance_plan_show_form()

    return render(request, 'Management/create_plan.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Admin, Secretory, Expert)
def view_plan(request, pid):
    plan = get_object_or_404(Insurance_plan, pk=pid)
    form = Insurance_plan_show_form(instance=plan)
    return render(request, 'Management/view_plan.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'plan_id': pid,
        'property_list': get_property_list(plan, form, id=plan.id),
    })


@login_required
def edit_plan(request, pid):
    success_message = None
    form = None

    plan = get_object_or_404(Insurance_plan, pk=pid)
    if request.method.upper() == 'POST':
        form = Insurance_plan_show_form(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            success_message = "Changes applied."
    else:
        form = Insurance_plan_show_form(instance=plan)

    return render(request, 'Management/edit_plan.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'plan_id': pid,
        'success_message': success_message,
    })


@login_required
@group_required(Admin)
def delete_plan(request, pid):
    plan = get_object_or_404(Insurance_plan, pk=pid)

    if request.method.upper() == 'POST':
        plan.delete()
        return redirect('Management:plan')

    return render(request, 'Management/delete_plan.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'plan': plan,
    })
