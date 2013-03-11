from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from Accident.forms import accident_form_show

from Insurance.models import *
from Insurance.forms import *
from Pasargad.helper import *

import os
import StringIO

from xhtml2pdf import pisa

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import escape


def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))

        if not os.path.isfile(path):
            path = os.path.join(settings.MEDIA_ROOT,
                                uri.replace(settings.MEDIA_URL, ""))

            if not os.path.isfile(path):
                raise Exception(
                    'media urls must start with %s or %s' % (
                        settings.MEDIA_ROOT, settings.STATIC_ROOT))

    return path


def render_to_pdf(template_src, context_dict):
    """Function to render html template into a pdf file"""
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                            dest=result,
                            encoding='UTF-8',
                            link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(result.getvalue(),
                                mimetype='application/pdf')

        return response

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


@login_required
@group_required(Secretory, Expert)
def home(request):
    return render(request, 'Insurance/home.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
    })


@login_required
@group_required(Secretory, Expert)
def contract(request):
    form = None
    if request.method.upper() == 'POST':
        form = Contract_search(request.POST)
        if form.is_valid():
            return redirect('Insurance:view_contract', cid=form.cleaned_data['contract'])
    else:
        form = Contract_search()

    return render(request, 'Insurance/enter_contract.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
    })


@login_required
@group_required(Secretory, Expert)
def view_contract(request, cid):
    print('here')
    contract_info = get_object_or_404(Contract, pk=cid).get_last_info()
    form = Contract_info_form_show(instance=contract_info)

    return render(request, 'Insurance/contract.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'property_list': get_property_list(contract_info, form, title='Contract', id=cid),
        'contract_info': get_contract_info(cid),
    })


@login_required
@group_required(Secretory)
def print_contract(request, cid):
    """Build briefing packages format and export as HTML and PDF."""
    contract_info = get_object_or_404(Contract, pk=cid).get_last_info()
    vehicle = contract_info.contract.vehicle
    vehicle_owner = vehicle.vehicle_owner
    person = vehicle_owner.person
    company = vehicle_owner.company

    property_set = [get_property_list(contract_info, Contract_info_form_show(), id=cid, title='Contract'),
                    get_property_list(vehicle.get_last_info(), Vehicle_info_form_show(), id=vehicle.id, title='Vehicle'),
                    get_property_list(vehicle_owner, vehicle_owner_form_show(), id=vehicle_owner.id,
                                      title='Vehicle Owner')]

    if person != None:
        property_set.append(get_property_list(person.get_last_info(), Person_info_form_show(), id=person.id, title='Person'))

    if company != None:
        property_set.append(get_property_list(company.get_last_info(), Company_info_form_show(), id=company.id, title='Company'))

    # return render(request, 'Insurance/pdf.html', {
    #     'property_set': property_set,
    # })

    return render_to_pdf('Insurance/pdf.html', {
        'property_set': property_set,
    })


@login_required
@group_required(Secretory, Expert)
def list_accident(request, cid):
    contract = get_object_or_404(Contract, pk=cid)
    queryset = contract.vehicle.accident_set.all().order_by('-date')[:10]
    form_head = accident_form_show()
    property_set = []
    for item in queryset:
        property_set.append(get_property_list(item, form_head, id=item.id))

    return render(request, 'Insurance/list_accident.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "There isn't any accident " if len(property_set) == 0 else '',
    })


@login_required
@group_required(Secretory)
def search_contract(request):
    form = None
    form_head = None
    property_set = []
    if request.method.upper() == 'POST':
        form = search_contract_form(request.POST)
        if form.is_valid():
            form_head = Contract_info_form_show()
            chassis_number = form.cleaned_data['chassis_number']
            queryset = Contract.objects.all().filter(vehicle__vehicle_info__chassis_number=chassis_number).distinct()
            for item in queryset:
                property_set.append(get_property_list(item.get_last_info(), form_head, id=item.id))
            form = None
    else:
        form = search_contract_form();

    return render(request, 'Insurance/search_contract.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "Thers isn't any vehicle with with this Chasiss number" if len(
            property_set) == 0 and form == None else '',
    })


@login_required
@group_required(Secretory)
def edit_contract(request, cid):
    success_message = None
    notify_message = None
    form = None

    contract_info = get_object_or_404(Contract, pk=cid).get_last_info()
    if request.method.upper() == 'POST':
        payment = Payment(cost=0, date=timezone.now(), dealer=request.user,
                          owner=contract_info.contract.vehicle.vehicle_owner)
        payment.save()
        contract_instance = Contract_info(contract=contract_info.contract, creation_date=timezone.now(),
                                          contract_type='A', payment=payment)
        form = Contract_info_form_edit(request.POST, instance=contract_instance)
        if form.is_valid():
            new_contract_info = form.save(commit=False)
            payment.cost = compute_different_payment(new_contract_info, contract_info)
            payment.save()
            new_contract_info.save()
            notify_message = 'you {} {} Rials at {}.'.format('paid' if payment.cost >= 0 else 'received',
                                                             abs(payment.cost),
                                                             payment.date)
            success_message = "Changes applied."
        else:
            payment.delete()
    else:
        form = Contract_info_form_edit(instance=contract_info)

    return render(request, 'Insurance/edit_contract.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form': form,
        'notify_message': notify_message,
        'success_message': success_message,
    })


@login_required
@group_required(Secretory)
def create_contract(request):
    form = None
    success_message = ''
    notify_message = ''
    hidden_table = dict()
    next_level = level = 0
    type_of_page = ''
    vehicle_owner = None
    vehicle = None
    contract_id = None

    if request.method.upper() == 'GET':
        form = Create_contract_first()
        next_level = 1
    else:
        level = int(request.POST['level'])
        next_level = level + 1

        if level == 1:
            form = Create_contract_first(request.POST)
            if form.is_valid():
                type_of_page = form.cleaned_data['drop_down']

                if type_of_page == 'Person':
                    form = Person_info_form_edit()
                elif type_of_page == 'Company':
                    form = Company_info_form_edit()
                else:
                    form = Get_vehicle_owner()
            else:
                next_level = 1

        elif level == 2:
            type_of_page = request.POST['type_of_page']
            if type_of_page == 'Person':
                person = Person()
                person.save()
                person_info_instance = Person_info(person=person, creation_date=timezone.now())
                form = Person_info_form_edit(request.POST, instance=person_info_instance)
                if form.is_valid():
                    form.save()
                    vehicle_owner = Vehicle_owner(person=person)
                    vehicle_owner.save()
                else:
                    person.delete()
                    next_level = level
            elif type_of_page == 'Company':
                company = Company()
                company.save()
                company_info_instance = Company_info(company=company, creation_date=timezone.now())
                form = Company_info_form_edit(request.POST, instance=company_info_instance)
                if form.is_valid():
                    form.save()
                    vehicle_owner = Vehicle_owner(company=company)
                    vehicle_owner.save()
                else:
                    company.delete()
                    next_level = level
            else:
                try:
                    form = Get_vehicle_owner(request.POST)
                    if form.is_valid():
                        vehicle_owner = Vehicle_owner.objects.all().get(id=form.cleaned_data['owner'])
                    else:
                        next_level = level
                except:
                    next_level = level

            if next_level != level:
                form = Vehicle_info_form_edit()

        elif level == 3:
            vehicle_owner = Vehicle_owner.objects.get(id=request.POST['vehicle_owner'])
            vehicle = Vehicle(vehicle_owner=vehicle_owner)
            vehicle.save()
            vehicle_info_instance = Vehicle_info(vehicle=vehicle, creation_date=timezone.now())
            form = Vehicle_info_form_edit(request.POST, instance=vehicle_info_instance)
            if form.is_valid():
                form.save()
                form = Contract_info_form_edit()
            else:
                vehicle.delete()
                next_level = level

        elif level == 4:
            vehicle = Vehicle.objects.get(id=request.POST['vehicle'])
            contract = Contract(vehicle=vehicle)
            contract.save()
            payment = Payment(cost=0, date=timezone.now(), dealer=request.user, owner=contract.vehicle.vehicle_owner)
            payment.save()
            contract_info_instance = Contract_info(contract=contract, creation_date=timezone.now(), contract_type='C',
                                                   payment=payment)
            form = Contract_info_form_edit(request.POST, instance=contract_info_instance)
            if form.is_valid():
                payment.cost = get_price(contract_info_instance)
                payment.save()
                form.save()
                form = None
                contract_id = contract.id
                notify_message = 'you {} {} Rials at {}.'.format('paid' if payment.cost >= 0 else 'received',
                                                                 abs(payment.cost), payment.date)
                success_message = "The Contract with {} has been saved.".format(contract_id)
            else:
                contract.delete()
                payment.delete()
                next_level = level

    if next_level == 2:
        hidden_table['type_of_page'] = type_of_page
    elif next_level == 3:
        hidden_table['vehicle_owner'] = vehicle_owner.id
    elif next_level == 4:
        hidden_table['vehicle'] = vehicle.id
    else:
        pass
    hidden_table['level'] = next_level

    return render(request, 'Insurance/create_contract.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'form': form,
        'hidden_table': hidden_table,
        'success_message': success_message,
        'notify_message': notify_message,
    })


@login_required
@group_required(Secretory, Expert)
def history_contract(request, cid):
    queryset = get_object_or_404(Contract, pk=cid).get_history()
    form_head = Contract_info_form_show()
    property_set = []
    for item in queryset:
        property_set.append(get_property_list(item, form_head, item.id))

    return render(request, 'Insurance/history_contract.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "There isn't any plan" if len(queryset) == 0 else '',
    })


@login_required
@group_required(Secretory)
def edit_company(request, cid, mid):
    success_message = None
    form = None

    company_info = get_object_or_404(Company, pk=mid).get_last_info()
    if request.method.upper() == 'POST':
        company_instance = Company_info(company=company_info.company, creation_date=timezone.now())
        form = Company_info_form_edit(request.POST, instance=company_instance)
        if form.is_valid():
            form.save()
            success_message = "Changes applied."
    else:
        form = Company_info_form_edit(instance=company_info)

    return render(request, 'Insurance/edit_company.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Secretory, Expert)
def view_company(request, cid, mid):
    company_info = get_object_or_404(Company, pk=mid).get_last_info()
    form = Company_info_form_show(instance=company_info)

    return render(request, 'Insurance/company.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'property_list': get_property_list(company_info, form, id=mid),
    })


@login_required
@group_required(Secretory, Expert)
def history_company(request, cid, mid):
    queryset = get_object_or_404(Company, pk=mid).get_history()
    form_head = Company_info_form_show()
    property_set = []
    for item in queryset:
        property_set.append(get_property_list(item, form_head, item.id))

    return render(request, 'Insurance/history_company.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "There isn't any plan" if len(queryset) == 0 else '',
    })


@login_required
@group_required(Secretory)
def edit_person(request, cid, pid):
    success_message = None
    form = None

    person_info = get_object_or_404(Person, pk=pid).get_last_info()
    if request.method.upper() == 'POST':
        person_instance = Person_info(person=person_info.person, creation_date=timezone.now())
        form = Person_info_form_edit(request.POST, instance=person_instance)
        if form.is_valid():
            form.save()
            success_message = "Changes applied."
    else:
        form = Person_info_form_edit(instance=person_info)

    return render(request, 'Insurance/edit_person.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Secretory, Expert)
def view_person(request, cid, pid):
    person_info = get_object_or_404(Person, pk=pid).get_last_info()
    form = Person_info_form_show(instance=person_info)

    return render(request, 'Insurance/person.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'property_list': get_property_list(person_info, form, id=pid),
    })


@login_required
@group_required(Secretory, Expert)
def history_person(request, cid, pid):
    queryset = get_object_or_404(Person, pk=pid).get_history()
    form_head = Person_info_form_show()
    property_set = []
    for item in queryset:
        property_set.append(get_property_list(item, form_head, item.id))

    return render(request, 'Insurance/history_person.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "There isn't any plan" if len(queryset) == 0 else '',
    })


@login_required
@group_required(Secretory)
def edit_vehicle(request, cid, vid):
    success_message = None
    form = None

    vehicle_info = get_object_or_404(Vehicle, pk=vid).get_last_info()
    if request.method.upper() == 'POST':
        vehicle_instance = Vehicle_info(vehicle=vehicle_info.vehicle, creation_date=timezone.now())
        form = Vehicle_info_form_edit(request.POST, instance=vehicle_instance)
        if form.is_valid():
            form.save()
            success_message = "Changes applied."
    else:
        form = Vehicle_info_form_edit(instance=vehicle_info)

    return render(request, 'Insurance/edit_vehicle.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form': form,
        'success_message': success_message,
    })


@login_required
@group_required(Secretory, Expert)
def view_vehicle(request, cid, vid):
    vehicle_info = get_object_or_404(Vehicle, pk=vid).get_last_info()
    form = Vehicle_info_form_show(instance=vehicle_info)

    return render(request, 'Insurance/vehicle.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'property_list': get_property_list(vehicle_info, form, id=vid),
    })


@login_required
@group_required(Secretory, Expert)
def history_vehicle(request, cid, vid):
    queryset = get_object_or_404(Vehicle, pk=vid).get_history()
    form_head = Vehicle_info_form_show()
    property_set = []
    for item in queryset:
        property_set.append(get_property_list(item, form_head, item.id))

    return render(request, 'Insurance/history_vehicle.html', {
        'user_name': get_user_name(request),
        'security': get_security(request),
        'contract_info': get_contract_info(cid),
        'form_head': form_head,
        'property_set': property_set,
        'notify_message': "There isn't any plan" if len(queryset) == 0 else '',
    })