__author__ = 'Behnam'
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from Insurance.models import *


class Insurance_type_show_form(ModelForm):
    class Meta:
        model = Insurance_type
        exclude = ()


class Insurance_type_edit_form(ModelForm):
    class Meta:
        model = Insurance_type
        exclude = ('id', )


class Insurance_plan_show_form(ModelForm):
    class Meta:
        model = Insurance_plan
        exclude = ('id', )


class Insurance_plan_edit_form(ModelForm):
    class Meta:
        model = Insurance_plan
        exclude = ('id', )
