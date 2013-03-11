__author__ = 'Behnam Hatami'
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _

from Insurance.models import *


class accident_form_show(ModelForm):
    class Meta:
        model = Accident
        exclude = ('id', 'payment')


class payment_form_show(ModelForm):
    class Meta:
        model = Payment
        exclude = ('id', )


class report_form_show(ModelForm):
    class Meta:
        model = Report
        exclude = ('id', )


class report_form_edit(ModelForm):
    class Meta:
        model = Report
        exclude = ('id', 'date', 'accident')


class search_accident_form(forms.Form):
    error_messages = {
        'not_exist': _("No Accident with this ID exists."),
    }

    accident = forms.IntegerField(required=True)

    def clean_accident(self):
        accident = self.cleaned_data["accident"]
        if accident:
            try:
                Accident.objects.get(pk=accident)
            except:
                raise forms.ValidationError(self.error_messages['not_exist'])
        return accident


class accident_form_create(ModelForm):
    class Meta:
        model = Accident
        exclude = ('payment',)
        widgets = {
            'vehicle': TextInput(),
        }
