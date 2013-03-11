from django.core.exceptions import ObjectDoesNotExist
from Statistic.utils import year_month_truncate, year_truncate

__author__ = 'Behnam Hatami'

from django import forms
from django.utils.translation import ugettext_lazy as _
from dateutil.relativedelta import relativedelta
from Insurance.models import *


class general_form(forms.Form):
    error_messages = {
        'rel_date': _("Start time should be before end time."),
        'single_day': _("You can not view chart of single day"),
        'single_month': _("You can not view chart of single month"),
        'single_year': _("You can not view chart of single year"),
        'multi_day': _("You can get chart of at most 30 days"),
        'multi_month': _("You can get chart of at most 30 months"),
        'multi_year': _("You can get chart of at most 30 years"),
    }

    type = forms.ChoiceField(
        choices=(('D', 'Daily'), ('M', 'Monthly'), ('Y', 'Yearly')), required=True)
    from_date = forms.DateField(label=_('From Date:'), required=True,
                                validators=[not_in_future_date])
    to_date = forms.DateField(label=_('To Date:'), required=True,
                              validators=[not_in_future_date])

    def clean(self):
        cleaned_data = super(general_form, self).clean()
        if 'to_date' not in cleaned_data or 'from_date' not in cleaned_data:
            return cleaned_data
        from_date = cleaned_data['from_date']
        to_date = cleaned_data['to_date']
        type = cleaned_data['type']

        if type == 'M':
            cleaned_data['from_date_trunc'] = year_month_truncate(from_date)
            cleaned_data['to_date_trunc'] = year_month_truncate(to_date)
        elif type == 'Y':
            cleaned_data['from_date_trunc'] = year_truncate(from_date)
            cleaned_data['to_date_trunc'] = year_truncate(to_date)
        elif type == 'D':
            cleaned_data['from_date_trunc'] = from_date
            cleaned_data['to_date_trunc'] = to_date

        if to_date < from_date:
            raise forms.ValidationError(self.error_messages['rel_date'])

        from_date = cleaned_data['from_date_trunc']
        to_date = cleaned_data['to_date_trunc']

        if type == 'D':
            if from_date == to_date:
                raise forms.ValidationError(self.error_messages['single_day'])
            if from_date + relativedelta(days=+30) < to_date:
                raise forms.ValidationError(self.error_messages['multi_day'])

            cleaned_data['time_delta'] = relativedelta(days=+1)
        elif type == 'M':
            if from_date == to_date:
                raise forms.ValidationError(self.error_messages['single_month'])

            if from_date + relativedelta(months=30) < to_date:
                raise forms.ValidationError(self.error_messages['multi_month'])

            cleaned_data['time_delta'] = relativedelta(months=+1)
        elif type == 'Y':
            if from_date == to_date:
                raise forms.ValidationError(self.error_messages['single_year'])

            if from_date + relativedelta(years=+1) == to_date:
                raise forms.ValidationError(self.error_messages['multi_year'])

            cleaned_data['time_delta'] = relativedelta(years=+1)
        return cleaned_data


class user__form(general_form):
    my_error_messages = {
        'invalid_user': _('No user with this id exists.')
    }
    user = forms.IntegerField(label=_('Username ID'), required=True)

    def clean_user(self):
        user = self.cleaned_data['user']
        try:
            return User.objects.get(pk=user)
        except ObjectDoesNotExist:
            raise forms.ValidationError(self.my_error_messages['invalid_user'])

class owner__form(general_form):
    my_error_messages = {
        'invalid_owner': _('No owner with this id exists.')
    }
    owner = forms.IntegerField(label=_('Owner ID'), required=True)

    def clean_owner(self):
        owner = self.cleaned_data['owner']
        try:
            return Vehicle_owner.objects.get(pk=owner)
        except ObjectDoesNotExist:
            raise forms.ValidationError(self.my_error_messages['invalid_owner'])

