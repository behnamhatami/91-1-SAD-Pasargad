__author__ = 'Behnam Hatami'

from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from Insurance.models import *


class Person_info_form_show(ModelForm):
    class Meta:
        model = Person_info
        exclude = ('id', 'person', )


class Person_info_form_edit(ModelForm):
    class Meta:
        model = Person_info
        exclude = ('id', 'person', 'creation_date')


class Company_info_form_show(ModelForm):
    class Meta:
        model = Company_info
        exclude = ('id', 'company',)


class Company_info_form_edit(ModelForm):
    class Meta:
        model = Company_info
        exclude = ('id', 'company', 'creation_date')


class Vehicle_owner_form(ModelForm):
    class Meta:
        model = Vehicle_owner
        exclude = ('id',)


class Vehicle_info_form_show(ModelForm):
    class Meta:
        model = Vehicle_info
        exclude = ('id', 'vehicle',)


class Vehicle_info_form_edit(ModelForm):
    class Meta:
        model = Vehicle_info
        exclude = ('id', 'vehicle', 'creation_date')


class Contract_info_form_show(ModelForm):
    class Meta:
        model = Contract_info
        exclude = ('id', 'contract', )


class Contract_info_form_edit(ModelForm):
    class Meta:
        model = Contract_info
        exclude = ('id', 'contract', 'creation_date', 'contract_type', 'payment')


class Contract_search(forms.Form):
    error_messages = {
        'not_exist': _("No Contract with this ID exists."),
    }
    contract = forms.IntegerField(required=True)

    def clean_contract(self):
        contract = self.cleaned_data['contract']
        if contract:
            try:
                Contract.objects.get(pk=contract)
            except:
                raise forms.ValidationError(self.error_messages['not_exist'])
        return contract


class Contract_info_form_edit(ModelForm):
    class Meta:
        model = Contract_info
        exclude = ('id', 'contract', 'creation_date', 'contract_type', 'payment')


class Create_contract_first(forms.Form):
    drop_down = forms.ChoiceField(
        choices=(('Person', 'Person'), ('Company', 'Company'), ('Existing owner', 'Existing owner')), required=True)


class Get_vehicle_owner(forms.Form):
    error_messages = {
        'not_exist': _("No Vehicle with this ID exists."),
    }

    owner = forms.IntegerField(required=True)

    def clean_owner(self):
        owner = self.cleaned_data['owner']
        if owner:
            try:
                Vehicle_owner.objects.get(pk=owner)
            except:
                raise forms.ValidationError(self.error_messages['not_exist'])
        return owner

class search_contract_form(forms.Form):
    chassis_number = forms.CharField(max_length=17, required=True)

class vehicle_owner_form_show(ModelForm):
    class Meta:
        model = Vehicle_owner
        exclude = ('id', )
