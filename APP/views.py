from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from .forms import RegistrationForm,Temp,LoginForm,Event,EventCreateForm,EventSearchForm
from django.views.generic.edit import FormView
from django.utils.encoding import force_text
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .tokens import account_activation_token
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Student,Staff,Roles,CustomUser,Organizer,EventsRegister
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage
from django.db.models import Q

def register(request):
    form = RegistrationForm(request.POST)
    temp = Temp(request.POST)
    if request.method == "POST":
        if form.is_valid() and temp.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            email = form.cleaned_data.get('email')
            print("form is valid")
            dept = temp.cleaned_data.get('dept')
            usertype = temp.cleaned_data.get('usertype')
            class1 = temp.cleaned_data.get('class1')
            rollno = temp.cleaned_data.get('rollno')

            is_head = temp.cleaned_data.get('is_head')
            if is_head=='YES':
                is_head =True
            else:
                is_head = False
            soc_head = temp.cleaned_data.get('soc_head')

            print(is_head,soc_head)
            print(dept,usertype)
            if User.objects.filter(email=email):
                messages.success(request, message='This email is already registered. Enter different email or login into your acccount')

            if usertype=='STAFF':
                print("its a staff")
                user.is_staff = True
                user.save()
                Staff.objects.create(user=user,dept=dept,role_id=Roles.objects.get(id=19),email_confirmed=False)
            else:
                print("its a student")
                Student.objects.create(user=user,classs=class1,dept=dept,role_id=Roles.objects.get(id=1),email_confirmed=False,is_head=is_head,soc_head=soc_head,class1=class1,rollno=rollno)
            current_site = get_current_site(request)
            print(current_site)


            mail_subject = 'Activate your account.'
            message = render_to_string('APP/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            user = ""
            print("Conform your email")
            messages.success(request, ('Please Confirm your email to complete registration.'))
            return HttpResponseRedirect(reverse('login'))
        else:
            print("else1")
            form = RegistrationForm(request.POST)
            temp = Temp(request.POST)
            return render(request, 'register.html', {'form': form, 'temp': temp})
    else:
        form = RegistrationForm()
        temp = Temp()
        return render(request, 'register.html', {'form': form,'temp':temp})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if user.is_staff:
            S = Staff.objects.get(user=user)
            S.email_confirmed = 1
        else:
            S = Student.objects.get(user=user)
            S.email_confirmed=1
        S.save()
        user.is_active = True
        user.save()
        messages.success(request, ('Your account have been confirmed.'))
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Activation link is invalid!')

def login(request):
    context={}
    if request.method =="POST":
        loginvar = LoginForm(request.POST)
        if loginvar.is_valid():
            email = request.POST['Email']
            password = request.POST['password']
            user = auth.authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                if user.is_staff:
                    S = Staff.objects.get(user=user)
                else:
                    S = Student.objects.get(user=user)
                if S.email_confirmed==0:
                    messages.success(request, ('Please Confirm your email first.'))
                    return HttpResponseRedirect(reverse('login'))
                if S.email_confirmed==1:
                    if user.is_active:
                        auth.login(request,user)
                        print("you are now logined")
                        return HttpResponseRedirect(reverse('ehomepage'))
                    else:
                        print("User not active")
                        context['err']="User not active"
                        return render(request,'login.html',context=context)
            else:
                loginvar = LoginForm()
                print("Provide valid 2credentials")
                messages.error(request, 'Invalid Login Credentials, Please Try Again')
                return render(request, 'login.html', context={"form": loginvar,"hello":3})
    else:
        print("else block")
        loginvar = LoginForm()
        return render(request=request, template_name="login.html", context={"form": loginvar,"hello":3})


@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    print("logged out")
    context={}
    context['msg']="you hav been loggedout login again"
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url="/login/")
def homepage1(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            return render(request=request, template_name="ehomepage.html")
        else:
            return render(request=request, template_name="homepage.html")
    else:
        return HttpResponseRedirect(reverse('login'))
@login_required(login_url='/login/')
def EventForApproval(request):
    user = User.objects.get(id=request.user.id)
    print(user.id)
    if user.is_staff:
        staff = Staff.objects.get(user_id=user.id)
        print(staff.role_id_id)
        role=Roles.objects.get(id=staff.role_id_id)
        organizer = Organizer.objects.get(role_id=role.id)
        events = Event.objects.filter(organizer=organizer)
        return render(request=request, template_name="eventapprove.html", context={'events': events})
    else:
        return HttpResponseRedirect(reverse('ehomepage'))

@login_required(login_url='/login/')
def approve(request,id):
    user = User.objects.get(id=request.user.id)
    print(user.id)
    if user.is_staff:
        event = Event.objects.get(id=id)
        event.is_approved=True
        staff = Staff.objects.get(user_id=user.id)
        print(staff.role_id_id)
        role = Roles.objects.get(id=staff.role_id_id)
        organizer = Organizer.objects.get(role_id=role.id)
        event.organizer = organizer
        event.save()
        return HttpResponseRedirect(reverse('ehomepage'))
    else:
        return HttpResponseRedirect(reverse('ehomepage'))

@login_required(login_url="/login/")
def EventHomepage(request):
    u = User.objects.get(id=request.user.id)
    print(u.id)
    shead = False
    try:
        s = Student.objects.get(user_id=request.user.id)
        shead = s.is_head
    except:
        pass
    isAllow = False
    if u.is_staff or shead:
        isAllow = True
    eventsearch = EventSearchForm(request.POST)
    if request.method == 'POST':
        if eventsearch.is_valid():
            typeofevent = eventsearch.cleaned_data.get('typeofevent')
            if typeofevent=='ALL':
                paginator = Paginator(Event.objects.filter(is_approved=True), 10)
            else:
                paginator = Paginator(Event.objects.filter(is_approved=True,event_type = typeofevent), 10)
            page = request.GET.get('page', 1)
            try:
                events = paginator.page(page)
            except PageNotAnInteger:
                events = paginator.page(1)
            except EmptyPage:
                events = paginator.page(paginator.num_pages)
            print(isAllow)
            return render(request, 'eventlist.html', context={"eventsearchform":eventsearch,"events": events, "isAllow": isAllow})
        else:
            eventsearch = EventSearchForm(request.POST)
            paginator = Paginator(Event.objects.all(), 10)
            page = request.GET.get('page', 1)
            try:
                events = paginator.page(page)
            except PageNotAnInteger:
                events = paginator.page(1)
            except EmptyPage:
                events = paginator.page(paginator.num_pages)
            print(isAllow)
            return render(request, 'eventlist.html', context={"eventsearchform":eventsearch,"events": events, "isAllow": isAllow})
    else:
        eventsearch = EventSearchForm()
        paginator = Paginator(Event.objects.all(), 10)
        page = request.GET.get('page', 1)
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)
        print(isAllow)
        return render(request, 'eventlist.html',
                      context={"eventsearchform": eventsearch, "events": events, "isAllow": isAllow})

    #     form = EventSearchForm(request.POST)
    #     if request.method == "POST":
    #         if form.is_valid():
    #             title = form.cleaned_data.get('title')
    #         else:
    #             form = EventSearchForm(request.POST)
    #             messages.error(request, 'Invalid Eventform')
    #             return render(request, 'EventHomePage.html', context={"form": form})
    #     else:
    #         print("http rsponse error in else")
    #         form = EventSearchForm()
    #         return render(request, template_name="EventHomePage.html", context={'form': form})
    # else:
    #     return HttpResponseRedirect(reverse('login'))
@login_required(login_url='/login/')
def eventRegister(request,id):
    print(id)
    print("inside")
    event = Event.objects.get(id=id)
    print(event.id)
    user = User.objects.get(id=request.user.id)
    student = Student.objects.get(user_id=user.id)

    e=EventsRegister.objects.filter(event=event,student=student).count()
    if e>0:
        messages.add_message(request, "You have sucessfully registered for the event")
    else:
        EventsRegister.objects.create(event=event, student=student)
        print("added")
        messages.add_message(request, "You are already  registered for the event")

    print('created')
    return HttpResponseRedirect(reverse('ehomepage'))


@login_required(login_url='/login/')
def myRegisteredEvents(request):
    user = request.user
    student = Student.objects.get(user_id=user.id)
    event = EventsRegister.objects.filter(student=student)
    for e in event:
        events = Event.objects.filter(id=event.event_id)
    return render(request, template_name="RegisteredEvents.html", context={'events': events})


def eventAction(request,id,action):
    pass

@login_required(login_url="/login/")
def JobsForYou(request):
    r = request.user.id
    print(r)
    user = UserProfile.objects.get(id=1)
    skills = user.skills
    city = user.city

    paginator = Paginator(
        Jobs.objects.filter(Q(jobtitle__icontains=skills, location__icontains=city) | Q(location__icontains=city,
                                                                                        jobdescription__icontains=skills)),
        10)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = {
        'users': users,
        'user': request.user,
        # 'jobsearchform': jobsearchform,
    }
    return render(request, template_name='jobsforyou.html', context=context)

def eventDetail(request,id):
    event = Event.objects.get(id=id)
    context={
        'eventid':event.id,'eventtitle':event.title,'eventdescription':event.description,
        'eventorganizer': event.organizer, 'eventapprovedby': event.approved_by, 'eventdate':event.date
    }
    return render(request, template_name="eventdetail.html", context=context)

def createEvent(request):
    form = EventCreateForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            date = form.cleaned_data.get('date')
            event_type = form.cleaned_data.get('event_type')
            org = form.cleaned_data.get('organizer')
            print(title,description,date,event_type,org)
            organizer = Organizer.objects.get(name=org)

            Event.objects.create(title=title, description=description, date=date,
                                    event_type=event_type, organizer=organizer)
            messages.success(
                    messages.add_message(request, (
                        'Event Successfully Created Waiting For Approval')))
            return HttpResponseRedirect(reverse('createaevent'))
        else:
            form = EventCreateForm(request.POST)
            print("Provide valid")
            messages.error(request, 'Invalid Eventform')
            return render(request, 'addevent.html', context={"form": form})
    else:
        print("http rsponse error in else")
        form = EventCreateForm()
        context = {
            'form': form,
        }
        return render(request, template_name="addevent.html", context=context)


def assa(request):
    return render(request, template_name="index.html")

def eventHome(request):
    pass

def myEvents(request):
    #student registered events
    pass

def profile(request):
    #change password
    #change photo
    pass

def eventApprovalPage(request):
    pass
