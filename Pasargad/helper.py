import datetime

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from Insurance.models import Contract

__author__ = 'Behnam Hatami'

Admin = 'Admin'
Secretory = 'Secretory'
Expert = 'Expert'


def group_required(*group_names):
    """
        Requires user membership in at least one of the groups passed in.
    """

    def in_groups(u):
        if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
            return True
        else:
            raise PermissionDenied

    return user_passes_test(in_groups)


def get_security(request):
    user = request.user
    pr = {}
    for group in user.groups.all():
        pr[group.name] = True
    if Admin not in pr:
        pr[Admin] = False
    if Secretory not in pr:
        pr[Secretory] = False
    if Expert not in pr:
        pr[Expert] = False
    return pr


def get_price(new):
    days = (new.expire_date - datetime.date.today()).days
    return new.insurance_plan.get_cost(new.contract.vehicle, days)


def compute_different_payment(new, old):
    if old.expire_date >= new.expire_date:
        new.expire_date = old.expire_date
    days = (new.expire_date - old.expire_date).days
    today = datetime.date.today()
    if today > old.expire_date:
        days_to_expire = 0
    else:
        days_to_expire = (old.expire_date - today).days

    diff_till_now = new.insurance_plan.get_cost(new.contract.vehicle, days_to_expire) - old.insurance_plan.get_cost(
        new.contract.vehicle, days_to_expire)
    diff_till_new = new.insurance_plan.get_cost(new.contract.vehicle, days)
    return diff_till_new + diff_till_now


def get_contract_info(cid):
    contract = Contract.objects.get(pk=cid)
    vehicle = contract.vehicle
    vehicle_owner = vehicle.vehicle_owner
    company = vehicle_owner.company
    person = vehicle_owner.person
    context = {
        'contract': contract,
        'vehicle': vehicle,
    }
    if company:
        context['company'] = company

    if person:
        context['person'] = person

    return context


def get_user_name(request):
    return request.user.first_name if request.user.first_name != None and len(
        request.user.first_name) != 0 else request.user.username


class property_list:
    def __init__(self, ret, id, title):
        self.id = id
        self.ret = ret
        self.title = title

    def __iter__(self):
        return self.ret.__iter__()


def improve_name(name):
    return name.replace('_', ' ').capitalize()


def get_choice(choice, choice_set):
    for choice_item in choice_set:
        if choice_item[0] == choice:
            return choice_item[1]
    return None


def props(input, form):
    pr = {}
    for field in input._meta.fields:
        if field.name not in form.Meta.exclude:
            if field.choices:
                pr[field.name] = get_choice(getattr(input, field.name), field.choices)
            else:
                pr[field.name] = getattr(input, field.name)

    for field in input._meta.get_all_field_names():
        if field not in pr and field not in form.Meta.exclude:
            try:
                item_list = getattr(input, field)
                ans = []
                for item in item_list.all():
                    ans.append(str(item))
                pr[field] = '\n'.join(ans)
            except:
                pass
    return pr


def get_property_list(input, form, id=None, title=None):
    pr = props(input, form)
    ret = []
    for key in form.fields.keys():
        if key in pr.keys():
            ret.append((form.fields[key].label, pr[key]))
    return property_list(ret, id, title)


def get_old_property_list(input, form, id=None, title=None):
    pr = props(input, form)
    pr_new = {}
    for item in pr.items():
        pr_new[improve_name(item[0])] = item[1]
    ret = []
    for field in form.visible_fields():
        if field.label in pr_new:
            ret.append((field.label, pr_new[field.label]))
        else:
            for meta_field in input._meta.fields:
                if meta_field.verbose_name == field.label:
                    ret.append((field.label, pr_new[improve_name(meta_field.name)]))
                    break

    return property_list(ret, id, title)
