from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.db import models
from django.forms.models import ModelForm
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from .models import Event
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.forms import SelectDateWidget
from django.dispatch import receiver

def validate_email(value):
    if User.objects.filter(email=value):
        raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
    print(type(value))
    j=value.split('@')[1]
    print("js is ",j)
    print(j[-1:-11])
    if not j == 'ves.ac.in':

        raise forms.ValidationError(
            _('This is not an VESIT email, Use VESIT email to register')
        )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,max_length=40,validators=[validate_email],widget=forms.TextInput(attrs={
                'placeholder': 'Enter your email'
            }
        ))
    first_name = forms.CharField(required=True,max_length=40,widget=forms.TextInput(attrs={
                'placeholder': 'Enter first name'
            }
        ))
    last_name = forms.CharField(required=True,max_length=40,widget=forms.TextInput(attrs={
                'placeholder': 'Enter last name'
            }
        ))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
class Temp(forms.Form):
    departments = [
        ('MCA', 'MCA'),
        ('CMPN', 'CMPN'),
        ('INFT', 'INFT'),
        ('INST', 'INST'),
        ('AIML', 'AIML'),
    ]
    usertype1 = [
        ('STUDENT', 'STUDENT'),
        ('STAFF', 'STAFF'),
    ]
    is_head1=[('YES','YES'),('NO','NO')]
    commitites = [
        ('NONE', 'NONE'),
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
    soc_head = forms.ChoiceField(choices=commitites)
    class1 = forms.CharField(max_length=30,required=False,)
    rollno = forms.IntegerField(max_value=100,required=False)
    dept = forms.ChoiceField(choices=departments)
    usertype = forms.ChoiceField(choices=usertype1,widget=forms.RadioSelect)
    is_head = forms.ChoiceField(choices=is_head1,widget=forms.RadioSelect)


class LoginForm(forms.Form):
    Email = forms.EmailField(required=True, label='Enter your email', max_length=100)
    password = forms.CharField(required=True, label='Enter your password', widget=forms.PasswordInput())

class EventCreateForm(forms.Form):
    type = [
        ('HACKATHON', 'HACKATHON'),
        ('WORKSHOP', 'WORKSHOP'),
        ('WEBINAR', 'WEBINAR'),
        ('OTHER', 'OTHER'),
    ]
    organizers = [
        ('MCA_DEPT','MCA_DEPT'),('CMPN_DEPT', 'CMPN_DEPT'),('INFT_DEPT', 'INFT_DEPT'),
        ('INST_DEPT', 'INST_DEPT'), ('AIML_DEPT', 'AIML_DEPT'), ('CLASS_INCHARGE', 'CLASS_INCHARGE'),
        ('CSI_SOCIETY', 'CSI_SOCIETY'), ('IEEE_SOCIETY', 'IEEE_SOCIETY'), ('ISA_SOCIETY', 'ISA_SOCIETY'),
        ('ISTE_SOCIETY', 'ISTE_SOCIETY'), ('VESLIT_COUNCIL', 'VESLIT_COUNCIL'), ('ECELL_COUNCIL', 'ECELL_COUNCIL'),
        ('PHOTOCIRCLE_COUNCIL', 'PHOTOCIRCLE_COUNCIL'), ('SORT_COUNCIL', 'SORT_COUNCIL'), ('MUSIC_COUNCIL', 'MUSIC_COUNCIL'),
        ('SPORTS_COUNCIL', 'SPORTS_COUNCIL'), ('CULTURAL_COUNCIL', 'CULTURAL_COUNCIL')
    ]
    title = forms.CharField(required=True, max_length=40)
    description = forms.CharField(required=True, max_length=40)
    event_type = forms.ChoiceField(choices=type)
    organizer = forms.ChoiceField(choices=organizers)
    date = forms.DateTimeField(widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class EventSearchForm(forms.Form):
    type1 = [
        ('ALL','ALL'),
        ('HACKATHON', 'HACKATHON'),
        ('WORKSHOP', 'WORKSHOP'),
        ('WEBINAR', 'WEBINAR'),
        ('OTHER', 'OTHER'),
    ]
    typeofevent = forms.ChoiceField(choices=type1)
#class StudentProfile(forms.Form):
#    class1 =
#    rollno =
#    image =
#    contact no=
#class ProfileUpdateForm(ModelForm):
#    class Meta:
#        model = UserProfile
#        fields = ['image','skills','additionalinfo','city']

# class SavedJobsSearch(ModelForm):
#     class Meta:
#         model=Saved
#         fields = ['Jobtitle','Sortby']
#
# class InfoSearchForm(ModelForm):
#     jobtitle=forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder': 'ENTER JOBTITLE, DESIGNATION OR SKILL'}))
#     class Meta:
#         model=InfoSearch
#         fields=['jobtitle']
#
# class JobsSearchForm(ModelForm):
#     INTEGER_CHOICES = [tuple([x, x]) for x in range(0, 32)]
#     experience = forms.ChoiceField(required=False,choices=INTEGER_CHOICES)
#     SALARY_CHOICES = [
#         ('any', 'any'),
#         ('below1lac', 'Below >1 Lacs'),
#         ('1to3Lacs', '1-3'),
#         ('3to5lacs', '3-5'),
#         ('5to7lacs', '5-7'),
#         ('7to9lacs', '7-9'),
#         ('9to11lacs', '10-11'),
#         ('above11lacs', 'Above 11'),
#     ]
#   #  salary = forms.ChoiceField(required=False, choices=SALARY_CHOICES)
#     jobtitle=forms.CharField(required=True,max_length=20,widget=forms.TextInput(attrs={'placeholder': 'ENTER JOBTITLE, DESIGNATION OR SKILL'}))
#     DATE_POSTED_CHOICES = [
#         ('Anytime', 'Anytime'),
#         ('Within1day', 'Within 1 Day'),
#         ('Within1week', 'Within 1 Week'),
#         ('Within15days', 'Within 15 Days'),
#         ('WithinAMonth', 'Within A Month'),
#         ('Within3Months', 'Within 3 Months'),
#         ('Within6Months', 'Within 6 Months'),
#         ('Within1Year', 'Within 1 Year'),
#     ]
#    # dateposted = forms.ChoiceField(required=False, choices=DATE_POSTED_CHOICES)
#     companyname= forms.CharField(required=False,max_length=25,widget=forms.TextInput(attrs={'placeholder': 'ENTER COMPANY NAME'}))
#     skills=forms.CharField(required=False,max_length=30,widget=forms.TextInput(attrs={'placeholder': 'ENTER SKILLS'}))
#     NO_OF_JOBS = [
#         (10, '10'),
#         (30, '30'),
#         (50, '50'),
#         (100, '100'),
#     ]
#     noofjobs = forms.ChoiceField(required=False, choices=NO_OF_JOBS)
#     JOB_TYPES = [
#         ('FULL-TIME', 'FULL-TIME',),
#         ('PART-TIME', 'PART-TIME'),
#         ('INTERNSHIP', 'INTERNSHIP'),
#         ('CONTRACT', 'CONTRACT'),
#     ]
#    # jobtype = forms.ChoiceField(required=False, choices=JOB_TYPES)
#     location = forms.CharField(required=False,max_length=15,widget=forms.TextInput(attrs={'placeholder': 'ENTER LOCATION'}))
#
#     class Meta:
#         model = Jobs
#         fields = ['jobtitle','experience','location','companyname','skills','noofjobs']
#
#
# class ResumeMain(forms.ModelForm):
#     class Meta:
#         model=Resume
#         fields=('__all__')
