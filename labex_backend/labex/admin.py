from django.contrib import admin
from django import forms

from .models import (RobotController, User, Lab, Appointment)

# Register your models here.
class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        exclude = ()
        widgets = {
        }       

class LabAdmin(admin.ModelAdmin):
    form = LabForm
    suit_form_tabs = (
        ('general', 'General'),
    )
    list_display = ['lab_name', 'code', 'robot',  'date_time_slot', 'create_date', 'update_date']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ()
        widgets = {
        }       

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    suit_form_tabs = (
        ('general', 'General'),
    )
    list_display = ['email', 'name', 'surname', 'school', 'create_date', 'update_date']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ()
        widgets = {
        }       

class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    suit_form_tabs = (
        ('general', 'General'),
    )
    list_display = ['email', 'lab_code', 'create_date', 'update_date']

class RobotControllerForm(forms.ModelForm):
    class Meta:
        model = RobotController
        exclude = ()
        widgets = {
        }       

class RobotControllerAdmin(admin.ModelAdmin):
    form = RobotControllerForm
    suit_form_tabs = (
        ('general', 'General'),
    )
    list_display = ['controller_id', 'controller_name', 'lastest_command', 'create_date', 'update_date']


admin.site.register(User, UserAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(RobotController, RobotControllerAdmin)

