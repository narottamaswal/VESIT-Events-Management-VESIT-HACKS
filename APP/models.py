from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
# src/users/model.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import datetime
def validate_email(value):
    print(type(value),value)

    if User.objects.filter(email=value):
        raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))

    if not value[-1:11] == '@ves.ac.in':

        raise forms.ValidationError(
            _('This is not an VESIT email, Use VESIT email to register')
        )

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# src/users/model.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

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

    def __str__(self):
        return self.role_assigned

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name='student')
    dept = models.CharField(max_length=30, blank=False)
    role_id = models.ForeignKey(Roles,on_delete=models.CASCADE)
    email_confirmed = models.BooleanField()
    is_head = models.BooleanField(default=False)
    commitites = [
        ('NONE','NONE'),
        ('CSI_HEAD', 'CSI_HEAD'),
        ('IEEE_HEAD', 'IEEE_HEAD'),
        ('ISA_HEAD', 'ISA_HEAD'),
        ('ISTE_HEAD', 'ISTE_HEAD'),
        ('VESLIT_HEAD', 'VESLIT_HEAD'),
        ('ECELL_HEAD', 'ECELL_HEAD'),
        ('PHOTOCIRCLE_HEAD', 'PHOTOCIRCLE_HEAD'),
        ('SORT_HEAD', 'SORT_HEAD'),
        ('MUSIC_HEAD', 'MUSIC_HEAD'),
        ('SPORTS_HEAD', 'SPORTS_HEAD'),
        ('CULTURAL_HEAD', 'CULTURAL_HEAD')
    ]
    soc_head = models.CharField(choices=commitites,max_length=30,default="",blank=True)
    class1= models.CharField(max_length=30,blank=True)
    rollno = models.IntegerField(max_length=100,blank=True)
    def __str__(self):
        return self.user.first_name

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name='staff')
    dept = models.CharField(max_length=30,blank=False)
    role_id = models.ForeignKey(Roles,on_delete=models.CASCADE)
    email_confirmed = models.BooleanField()
    def __str__(self):
        return self.user.email

class Organizer(models.Model):
    role_id = models.ForeignKey(Roles,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    membership_required = models.BooleanField(default=0)

from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=30,blank=False)
    description = models.CharField(max_length=30,blank=False)
    date = models.DateTimeField(default=timezone.now())
    organizer = models.ManyToManyField(Organizer,blank=True)
    is_approved = models.BooleanField(default=False)
    type = [
        ('HACKATHON','HACKATHON'),
        ('WORKSHOP', 'WORKSHOP'),
        ('WEBINAR', 'WEBINAR'),
        ('OTHER','OTHER'),
    ]
    event_type = models.CharField(choices=type,max_length=30)
    approved_by = models.ForeignKey(Staff,on_delete=models.CASCADE,blank=True,default=1)
    def __str__(self):
        return self.title


class EventsRegister(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,blank=False)
    student = models.ManyToManyField(Student,blank=True)