import email
from shutil import _ntuple_diskusage
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, null=False, blank=False)
    role = models.TextField(null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    name = models.TextField(null=True, blank=False)
    surname = models.TextField(null=True, blank=False)
    school = models.TextField(null=True, blank=False)
    DOB = models.DateField(null=True, blank=False)
    password = models.TextField(null=True, blank=False)
    create_date = models.DateTimeField(verbose_name=('create_date'), null=True, blank=False, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=('update_date'), null=True, blank=False, auto_now=True)
    
    def __str__(self):
        return str(self.email) or "{}".format(self.email)



class RobotController(models.Model):
    controller_id = models.AutoField(primary_key=True, null=False, blank=False)
    controller_name = models.TextField(null=True, blank=False)
    lastest_command = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=('create_date'), null=True, blank=False, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=('update_date'), null=True, blank=False, auto_now=True)

    def __str__(self):
        return str(self.controller_id) or "controller_id {}".format(self.controller_id)

class Lab(models.Model):
    lab_id = models.AutoField(primary_key=True, null=False, blank=False)
    lab_name = models.TextField(null=True, blank=False)
    code = models.CharField(max_length=4, null=True, blank=False) 
    user_controller = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    robot = models.ForeignKey(RobotController, null=True, blank=False, on_delete=models.CASCADE)
    date_time_slot = models.DateTimeField(null=True, blank=False)
    create_date = models.DateTimeField(verbose_name=('create_date'), null=True, blank=False, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=('update_date'), null=True, blank=False, auto_now=True)

    def __str__(self):
        return str(self.lab_name) or "lab name {}".format(self.lab_name)

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True, null=False, blank=False)
    email =  models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    lab_code =  models.ForeignKey(Lab, null=True, blank=False, on_delete=models.CASCADE)    
    create_date = models.DateTimeField(verbose_name=('create_date'), null=True, blank=False, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=('update_date'), null=True, blank=False, auto_now=True)

    def __str__(self):
        return str(self.appointment_id) or "appointment_id {}".format(self.appointment_id)
