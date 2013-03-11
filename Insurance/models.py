from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def not_in_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('{} is in future'.format(value))


def not_in_future_datetime(value):
    if value > timezone.now():
        raise ValidationError('{} is in future'.format(value))


def in_the_future_date(value):
    if value < timezone.now().date():
        raise ValidationError('{} is in past'.format(value))


class Person(models.Model):
    def get_history(self):
        return self.person_info_set.order_by('-creation_date')

    def get_last_info(self):
        if len(self.get_history()) > 0:
            return self.get_history()[0]
        else:
            return None


    def __str__(self):
        if self.get_last_info() is not None:
            return self.get_last_info().__str__()
        else:
            return "{}".format(self.id)


class Person_info(models.Model):
    person = models.ForeignKey(Person)
    creation_date = models.DateTimeField(unique=True)

    gender_choices = {('M', 'Male'), ('F', 'Female')}
    pid = models.IntegerField(max_length=10, verbose_name='National Identification Number')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    father_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=gender_choices)
    date_of_birth = models.DateField(validators=[not_in_future_date])
    postal_code = models.IntegerField(max_length=10)
    address = models.TextField(max_length=256)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Company(models.Model):
    def get_history(self):
        return self.company_info_set.order_by('-creation_date')

    def get_last_info(self):
        if len(self.get_history()) > 0:
            return self.get_history()[0]
        else:
            return None


    def __str__(self):
        if self.get_last_info() is not None:
            return self.get_last_info().__str__()
        else:
            return "{}".format(self.id)


class Company_info(models.Model):
    company = models.ForeignKey(Company)
    creation_date = models.DateTimeField(unique=True)

    cid = models.IntegerField(max_length=10, verbose_name="Company Identification Number")
    name = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    register_date = models.DateField(validators=[not_in_future_date])

    def __str__(self):
        return "{}".format(self.name)


class Vehicle_owner(models.Model):
    person = models.ForeignKey(Person, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    def __str__(self):
        if self.person is None:
            return "{}".format(self.company)
        else:
            return "{}".format(self.person)


class Vehicle(models.Model):
    vehicle_owner = models.ForeignKey(Vehicle_owner)

    def get_history(self):
        return self.vehicle_info_set.order_by('-creation_date')

    def get_last_info(self):
        if len(self.get_history()) > 0:
            return self.get_history()[0]
        else:
            return None


    def __str__(self):
        if self.get_last_info() is not None:
            return self.get_last_info().__str__()
        else:
            return "{}".format(self.id)


class Vehicle_info(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    creation_date = models.DateTimeField(unique=True)

    fuel_type_choices = {('G', 'gasoline'), ('M', 'Methane'), ('P', 'Petrol')}
    chassis_number = models.CharField(max_length=17)
    motor_number = models.IntegerField(max_length=11)
    class_type = models.CharField(max_length=64)
    system_type = models.CharField(max_length=64)
    vehicle_type = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    fuel_type = models.CharField(max_length=1, choices=fuel_type_choices)
    cylinder = models.IntegerField(max_length=1)
    wheel = models.IntegerField(max_length=1)
    axis = models.IntegerField(max_length=1)
    price = models.IntegerField(max_length=10, help_text='enter price in Rial')
    production_date = models.DateField(validators=[not_in_future_date])

    def __str__(self):
        return "{} {}".format(self.vehicle_type, self.chassis_number)


class Payment(models.Model):
    cost = models.IntegerField(max_length=10)
    date = models.DateTimeField(validators=[not_in_future_datetime])
    dealer = models.ForeignKey(User)
    owner = models.ForeignKey(Vehicle_owner)

    def __str__(self):
        return '{}: {} at {}'.format(self.id, self.cost, self.date)


class Accident(models.Model):
    date = models.DateTimeField(validators=[not_in_future_datetime])
    description = models.TextField(max_length=1024)
    vehicle = models.ForeignKey(Vehicle)
    payment = models.ForeignKey(Payment, null=True, blank=True)

    def get_report(self):
        if len(self.report_set.all()) > 0:
            return self.report_set.all()[0]
        else:
            return None

    def __str__(self):
        return "{}: {}".format(self.id, self.date)


class Report(models.Model):
    date = models.DateTimeField(validators=[not_in_future_datetime])
    description = models.TextField(max_length=1024)
    cost = models.IntegerField(max_length=10, validators=[MinValueValidator(0)])
    accident = models.ForeignKey(Accident)

    def __str__(self):
        return "{}: {}".format(self.id, self.date)


class Insurance_type(models.Model):
    name = models.CharField(max_length=64, unique=True, validators=[MinLengthValidator(5)])
    cost = models.IntegerField(max_length=10,
                               validators=[MinValueValidator(0), MaxValueValidator(100 * 1000)],
                               help_text='enter number in milli percent')
    base_cost = models.IntegerField(max_length=10, validators=[MinValueValidator(0)], help_text='enter number in Rial')
    description = models.TextField(max_length=1024)

    def get_cost(self, vehicle):
        return (self.cost * vehicle.get_last_info().price) // 100000

    def get_base_cost(self):
        return self.base_cost

    def __str__(self):
        return "{}: {}".format(self.id, self.name)


class Insurance_plan(models.Model):
    name = models.CharField(max_length=64, unique=True, validators=[MinLengthValidator(5)])
    discount = models.IntegerField(max_length=10, validators=[MaxValueValidator(100 * 1000)],
                                   help_text='enter number in milli percent')
    insurance_types = models.ManyToManyField(Insurance_type)

    def get_cost(self, vehicle, days):
        cost = 0
        for insurance_type in self.insurance_types.all():
            cost += insurance_type.get_cost(vehicle) + insurance_type.get_base_cost()

        return cost * (100000 - self.discount) * days // 365 // 100000


    def __str__(self):
        return "{}: {}".format(self.id, self.name)


class Contract(models.Model):
    vehicle = models.ForeignKey(Vehicle)

    def get_history(self):
        return self.contract_info_set.order_by('-creation_date')

    def get_last_info(self):
        if len(self.get_history()) > 0:
            return self.get_history()[0]
        else:
            return None


    def __str__(self):
        if self.get_last_info() is not None:
            return self.get_last_info().__str__()
        else:
            return "{}".format(self.id)


class Contract_info(models.Model):
    contract_choices = {('C', 'Create Contract'), ('A', 'Attachment')}

    contract = models.ForeignKey(Contract)
    creation_date = models.DateTimeField(unique=True)
    contract_type = models.CharField(max_length=1, choices=contract_choices)
    expire_date = models.DateField(validators=[in_the_future_date])
    insurance_plan = models.ForeignKey(Insurance_plan)
    payment = models.ForeignKey(Payment)

    def __str__(self):
        return "{}: {}".format(self.id, self.expire_date)
