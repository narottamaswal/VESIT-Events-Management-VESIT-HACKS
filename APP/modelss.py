from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser


class Roles(models.Model):
    options = [
        ('STUDENT', 'STUDENT'),
        ('PRINCIPAL', 'PRINCIPAL'),
        ('MCA_HOD', 'PRINCIPAL'),
        ('CMPN_HOD', 'CMPN_HOD'),
         ('INFT_HOD', 'INFT_HOD'),
         ('INST_HOD', 'INST_HOD'),
         ('AIML_HOD', 'AIML_HOD'),
         ('COUNCIL_INCHARGE', 'COUNCIL_INCHARGE'),
        ('CSI_STAFF', 'CSI_STAFF'),
        ('IEEE_STAFF', 'IEEE_STAFF'),
         ('ISA_STAFF', 'ISA_STAFF'),
         ('ISTE_STAFF', 'ISTE_STAFF'),
         ('VESLIT_STAFF', 'VESLIT_STAFF'),
         ('ECELL_STAFF', 'ECELL_STAFF'),
         ('PHOTOCIRCLE_STAFF', 'PHOTOCIRCLE_STAFF'),
         ('SORT_STAFF', 'SORT_STAFF'),
         ('MUSIC_STAFF', 'MUSIC_STAFF'),
         ('SPORTS_STAFF', 'SPORTS_STAFF'),
         ('CULTURAL_STAFF', 'CULTURAL_STAFF')
         ]
 #   role = models.IntegerField()
    role_assigned = models.CharField(choices=options,max_length=100)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='student')
    classs = models.CharField(max_length=30, blank=False)
    dept = models.CharField(max_length=30, blank=False)
    role_id = models.ForeignKey(Roles,on_delete=models.CASCADE)
    email_confirmed = models.BooleanField()

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='staff')
    dept = models.CharField(max_length=30,blank=False)
    role_id = models.ForeignKey(Roles,on_delete=models.CASCADE)
    council_head = models.CharField(max_length=30,blank=False)
    email_confirmed = models.BooleanField()

class Organizer(models.Model):
    name = models.CharField(max_length=30)
    membership_required = models.BooleanField(default=0)

class Event(models.Model):
    title = models.CharField(max_length=30,blank=False)
    description = models.CharField(max_length=30,blank=False)
    date = models.DateTimeField()
    organizer = models.OneToOneField(Organizer,on_delete=models.CASCADE)
    type = [
        ('HACKATHON','HACKATHON'),
        ('WORKSHOP', 'WORKSHOP'),
        ('WEBINAR', 'WEBINAR'),
        ('OTHER','OTHER'),
    ]
    event_type = models.CharField(choices=type,max_length=30)
    approved_by = models.OneToOneField(Staff,on_delete=models.CASCADE)

