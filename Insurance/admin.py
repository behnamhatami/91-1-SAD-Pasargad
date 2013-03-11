__author__ = 'Behnam Hatami'

from django.contrib import admin
from Insurance.models import *

admin.site.register(Person)
admin.site.register(Person_info)
admin.site.register(Company)
admin.site.register(Company_info)
admin.site.register(Vehicle)
admin.site.register(Vehicle_info)
admin.site.register(Vehicle_owner)
admin.site.register(Payment)
admin.site.register(Accident)
admin.site.register(Report)
admin.site.register(Insurance_type)
admin.site.register(Insurance_plan)
admin.site.register(Contract)
admin.site.register(Contract_info)
