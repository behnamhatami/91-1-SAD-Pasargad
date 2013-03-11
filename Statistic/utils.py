__author__ = 'Behnam'

import datetime

from django.db.models.aggregates import Sum, Count
import pytz

from Pasargad.settings import TIME_ZONE


def date_filter(query_set, from_date, to_date):
    user_tz_preference = pytz.timezone(TIME_ZONE)
    from_date = datetime.datetime.combine(from_date, datetime.time.min).replace(tzinfo=user_tz_preference)
    to_date = datetime.datetime.combine(to_date, datetime.time.max).replace(tzinfo=user_tz_preference)
    return query_set.filter(date__lte=to_date).filter(date__gte=from_date)


def date_between_filter(query_set, from_date, to_date):
    user_tz_preference = pytz.timezone(TIME_ZONE)
    from_date = datetime.datetime.combine(from_date, datetime.time.min).replace(tzinfo=user_tz_preference)
    to_date = datetime.datetime.combine(to_date, datetime.time.min).replace(tzinfo=user_tz_preference)
    return query_set.filter(date__lt=to_date).filter(date__gte=from_date)


def year_truncate(from_date):
    return datetime.date(from_date.year, 1, 1)


def year_month_truncate(from_date):
    return datetime.date(from_date.year, from_date.month, 1)


def get_income(query_set):
    return normalize(query_set.filter(cost__gte=0).aggregate(Sum('cost'))[
        'cost__sum'])


def cut_str(inp, form_type):
    if form_type == 'D':
        return inp[5:]
    elif form_type == 'M':
        return inp[:7]
    elif form_type == 'Y':
        return inp[:4]
    else:
        return inp


def get_outcome(query_set):
    return normalize(query_set.filter(cost__lte=0).aggregate(Sum('cost'))[
        'cost__sum'])

def get_count(query_set):
    return normalize(query_set.count())

def normalize(inp):
    if inp:
        return abs(inp)
    else:
        return 0


def get_count_report(query_set, form):
    from_date = form.cleaned_data['from_date']
    to_date = form.cleaned_data['to_date']
    query_set = date_filter(query_set, from_date, to_date)
    from_date = form.cleaned_data['from_date_trunc']
    to_date = form.cleaned_data['to_date_trunc']
    time_delta = form.cleaned_data['time_delta']
    form_type = form.cleaned_data['type']
    ret = ([], [])
    while from_date <= to_date:
        new_from_date = from_date + time_delta
        loc_query_set = date_between_filter(query_set, from_date, new_from_date)
        ret[0].append(cut_str(from_date.__str__(), form_type))
        ret[1].append(get_count(loc_query_set))
        from_date = new_from_date

    return ret


def get_payment_report(query_set, form):
    from_date = form.cleaned_data['from_date']
    to_date = form.cleaned_data['to_date']
    query_set = date_filter(query_set, from_date, to_date)
    from_date = form.cleaned_data['from_date_trunc']
    to_date = form.cleaned_data['to_date_trunc']
    time_delta = form.cleaned_data['time_delta']
    form_type = form.cleaned_data['type']
    ret = ([], [], [])
    while from_date <= to_date:
        new_from_date = from_date + time_delta
        loc_query_set = date_between_filter(query_set, from_date, new_from_date)
        ret[0].append(cut_str(from_date.__str__(), form_type))
        ret[1].append(get_income(loc_query_set))
        ret[2].append(get_outcome(loc_query_set))
        from_date = new_from_date

    return ret
