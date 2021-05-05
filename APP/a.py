from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import JobsSearchForm, SavedJobsSearch, InfoSearchForm, ResumeMain
from .search import indeedsearch
from .models import Jobs, UserProfile, Temp, Example2, state, city
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from bs4 import BeautifulSoup
from django.forms import modelformset_factory
import datetime as dt
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db.models import Q
import os
from django.http import FileResponse

from django.conf import settings
import matplotlib

matplotlib.use('Agg')


# Create your views here.

@login_required(login_url="/login/")
def demo(request):
    return render(request, template_name="demo.html")

def resume(request):
    filepath = os.path.join("static", "images", 'resumeexample.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


def createyourresume(request):
    context = {}
    if request.method == "POST":
        ResumeForm = ResumeMain(request.POST, instance=request.user)
        if ResumeForm.is_valid():
            print("form is valid")
            instance = ResumeForm.save()
            name = ResumeForm.cleaned_data.get('name')
            print(name)
            email = ResumeForm.cleaned_data.get('email')
            phoneno = ResumeForm.cleaned_data.get('phoneno')
            linkedinprofileurl = ResumeForm.cleaned_data.get('linkedinprofileurl')
            usertitle = ResumeForm.cleaned_data.get('usertitle')
            skills = ResumeForm.cleaned_data.get('skills')
            extrainfo = ResumeForm.cleaned_data.get('extrainfo')
            address = ResumeForm.cleaned_data.get('address')
            # request.session.flush()
            request.session['address'] = ResumeForm.cleaned_data.get('address')
            request.session['projecttitle1'] = ResumeForm.cleaned_data.get('projecttitle1')
            request.session['projectdescription1'] = ResumeForm.cleaned_data.get('projectdescription1')
            request.session['projectyoc1'] = ResumeForm.cleaned_data.get('projectyoc1')
            request.session['projecttitle2'] = ResumeForm.cleaned_data.get('projecttitle2')
            request.session['projectdescription2'] = ResumeForm.cleaned_data.get('projectdescription2')
            request.session['projectyoc2'] = ResumeForm.cleaned_data.get('projectyoc2')
            request.session['projecttitle3'] = ResumeForm.cleaned_data.get('projecttitle3')
            request.session['projectdescription3'] = ResumeForm.cleaned_data.get('projectdescription3')
            request.session['projectyoc3'] = ResumeForm.cleaned_data.get('projectyoc3')

            request.session['companyname1'] = ResumeForm.cleaned_data.get('companyname1')
            request.session['designation1'] = ResumeForm.cleaned_data.get('designation1')
            request.session['companyyow1'] = ResumeForm.cleaned_data.get('companyyow1')
            request.session['companyname2'] = ResumeForm.cleaned_data.get('companyname2')
            request.session['designation2'] = ResumeForm.cleaned_data.get('designation2')
            request.session['companyyow2'] = ResumeForm.cleaned_data.get('companyyow2')
            request.session['companyname3'] = ResumeForm.cleaned_data.get('companyname3')
            request.session['designation3'] = ResumeForm.cleaned_data.get('designation3')
            request.session['companyyow3'] = ResumeForm.cleaned_data.get('companyyow3')

            request.session['institute1'] = ResumeForm.cleaned_data.get('institute1')
            request.session['degree1'] = ResumeForm.cleaned_data.get('degree1')
            request.session['stream1'] = ResumeForm.cleaned_data.get('stream1')
            request.session['studyforyears1'] = ResumeForm.cleaned_data.get('studyforyears1')
            request.session['grade1'] = ResumeForm.cleaned_data.get('grade1')
            request.session['institute2'] = ResumeForm.cleaned_data.get('institute2')
            request.session['degree2'] = ResumeForm.cleaned_data.get('degree2')
            request.session['stream2'] = ResumeForm.cleaned_data.get('stream2')
            request.session['studyforyears2'] = ResumeForm.cleaned_data.get('studyforyears2')
            request.session['grade2'] = ResumeForm.cleaned_data.get('grade2')
            request.session['institute3'] = ResumeForm.cleaned_data.get('institute3')
            request.session['degree3'] = ResumeForm.cleaned_data.get('degree3')
            request.session['stream3'] = ResumeForm.cleaned_data.get('stream3')
            request.session['studyforyears3'] = ResumeForm.cleaned_data.get('studyforyears3')
            request.session['grade3'] = ResumeForm.cleaned_data.get('grade3')
            request.session['name'] = str(name)
            request.session['email'] = str(email)
            request.session['phoneno'] = str(phoneno)
            request.session['linkedinprofileurl'] = str(linkedinprofileurl)
            request.session['usertitle'] = str(usertitle)
            request.session['skills'] = str(skills)
            request.session['extrainfo'] = str(extrainfo)
            a = resumegenerator(request)
            ResumeForm = ResumeMain(request.POST, instance=request.user)

            context = {'ResumeForm': ResumeForm}
            return render(request=request, template_name='createyourresume.html', context=context)
    else:
        print("else")
        ResumeForm = ResumeMain(request.POST, instance=request.user)
        context = {'ResumeForm': ResumeForm}
        return render(request=request, template_name='createyourresume.html', context=context)


def example(request):
    Example = modelformset_factory(model=Example2, fields=('name', 'location'))
    if request.method == "POST":
        form = Example(request.POST)
        instance = form.save()
    form = Example()
    context = {'form': form}
    return render(request, template_name='example.html', context=context)


def pdfview(request):
    image_data = open('static/images/resumeexample.pdf', 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')


def info(request):
    labels = []
    data = []
    indeed = 0
    shine = 0
    linkedin = 0
    freshersworld = 0
    timesjobs = 0
    minsal = 0
    maxsal = 0
    count = 0
    if request.method == "POST":
        infosearchform = InfoSearchForm(request.POST, instance=request.user)
        if infosearchform.is_valid():
            infosearchform.save()
            infosearchtitle = infosearchform.cleaned_data.get('jobtitle')
            print(infosearchtitle)
            # No of jobs posted on website(pie chart)
            queryset = Jobs.objects.filter(
                Q(jobtitle__icontains=infosearchtitle) | Q(jobdescription__icontains=infosearchtitle)).order_by(
                '-minsal')
            for i in queryset:
                print("hi")
                if "indeed" in str(i.jobportal).lower():
                    indeed += 1
                elif "linkedin" in str(i.jobportal).lower():
                    linkedin += 1
                elif "times jobs" in str(i.jobportal).lower():
                    timesjobs += 1
                elif "freshersworld" in str(i.jobportal).lower():
                    freshersworld += 1
                else:
                    shine += 1
            labels.append("Indeed")
            labels.append("Linkedin")
            labels.append("Times Jobs")
            labels.append("Freshersworld")
            labels.append("shine")
            data.append(indeed)
            data.append(linkedin)
            data.append(timesjobs)
            data.append(freshersworld)
            data.append(shine)

            # Top companies hiring the searched jobtitle
            companies = []
            openings = []
            c = 0
            for i in queryset:
                companies.append(i.companyname)
            # print(companies)
            for i in range(0, len(companies) - 1):
                if companies[i] == companies[i + 1]:
                    c += 2
                    openings.append(c)
                    c = 0
                else:
                    c += 1
                    openings.append(c)
                    c = 0
            companies = []
            for i in queryset:
                if not str(i.companyname) in companies:
                    companies.append(i.companyname)
            # print(openings)

            # location wise openings
            alllocations = []
            locations = []
            openingsloc = []
            c = 0
            fl = []
            for i in queryset:
                b = str(i.location).upper()
                alllocations.append(b)

            for j in alllocations:
                if '(' in j:
                    j.replace('(', '')
            # print(alllocations)

            s = ['AGARTALA', 'AGRA', 'AHMEDABAD', 'AIZWAL', 'AJMER', 'ALLAHABAD', 'ALLEPPEY', 'ALIBAUG', 'ALMORA',
                 'ALSISAR', 'ALWAR', 'AMBALA', 'AMLA', 'AMRITSAR', 'ANAND', 'ANKLESHWAR', 'ASHTAMUDI', 'AULI',
                 'AURANGABAD', 'BADDI', 'BADRINATH', 'BALASINOR', 'BALRAMPUR', 'BAMBORA', 'BANDHAVGARH', 'BANDIPUR',
                 'BANGALORE', 'BARBIL', 'BAREILLY', 'BEHROR', 'BELGAUM', 'BERHAMPUR', 'BETALGHAT', 'BHARATPUR',
                 'BHANDARDARA', 'BHARUCH', 'BHAVANGADH', 'BHAVNAGAR', 'BHILAI', 'BHIMTAL', 'BHOPAL', 'BHUBANESHWAR',
                 'BHUJ', 'BIKANER', 'BINSAR', 'BODHGAYA', 'BUNDI', 'CALICUT', 'CANANNORE', 'CHAIL', 'CHAMBA',
                 'CHANDIGARH', 'CHENNAI', 'CHIKMAGALUR', 'CHIPLUN', 'CHITRAKOOT', 'CHITTORGARH', 'COIMBATORE',
                 'COONOOR', 'COORG', 'CORBETT NATIONAL PARK', 'CUTTACK', 'DABHOSA', 'DALHOUSIE', 'DAMAN', 'DANDELI',
                 'DAPOLI', 'DARJEELING', 'DAUSA', 'DEHRADUN', 'DHARAMSHALA', 'DIBRUGARH', 'DIGHA', 'DIU', 'DIVE AGAR',
                 'DOOARS', 'DURGAPUR', 'DURSHET', 'DWARKA', 'FARIDABAD', 'FIROZABAD', 'GANGOTRI', 'GANGTOK',
                 'GANAPATIPULE', 'GANDHIDHAM', 'GANDHINAGAR', 'GARHMUKTESHWAR', 'GARHWAL', 'GAYA', 'GHAZIABAD', 'GOA',
                 'GOKHARNA', 'GONDAL', 'GORAKHPUR', 'GREATER NOIDA', 'GULMARG', 'GURGAON', 'GURUVAYOOR', 'GUWAHATI',
                 'GWALIOR', 'HALEBID', 'HAMPI', 'HANSI', 'HARIDWAR', 'HASSAN', 'HOSPET', 'HOSUR', 'HUBLI', 'HYDERABAD',
                 'IDUKKI', 'IGATPURI', 'IMPHAL', 'INDORE', 'JABALPUR', 'JAIPUR', 'JAISALMER', 'JALANDHAR', 'JALGAON',
                 'JAMBUGODHA', 'JAMMU', 'JAMNAGAR', 'JAMSHEDPUR', 'JAWHAR', 'JHANSI', 'JODHPUR', 'JOJAWAR', 'JORHAT',
                 'JUNAGADH', 'KABINI', 'KALIMPONG', 'KANATAL', 'KANCHIPURAM', 'KANHA', 'KANPUR', 'KANYAKUMARI',
                 'KARGIL', 'KARJAT', 'KARNAL', 'KARUR', 'KARWAR', 'KASARGOD', 'KASAULI', 'KASHIPUR', 'KASHID', 'KATRA',
                 'KAUSANI', 'KAZA', 'KAZIRANGA', 'KEDARNATH', 'KHAJJIAR', 'KHAJURAHO', 'KHANDALA', 'KHIMSAR', 'KOCHIN',
                 'KOCHI', 'KODAIKANAL', 'KOLHAPUR', 'KOLKATA', 'KOLLAM', 'KOTA', 'KOTAGIRI', 'KOTTAYAM', 'KOVALAM',
                 'KUFRI', 'KUMBALGARH', 'KULLU', 'KUMARAKOM', 'KUMBAKONAM', 'KUMILY', 'KURSEONG', 'KUSHINAGAR',
                 'LACHUNG', 'LEH', 'LAKSHADWEEP', 'LONAVALA', 'LOTHAL', 'LUCKNOW', 'LUDHIANA', 'LUMBINI', 'MADURAI',
                 'MAHABALESHWAR', 'MAHABALIPURAM', 'MALAPPURAM', 'MALPE', 'MALSHEJ GHAT', 'MALVAN', 'MANALI', 'MANDAVI',
                 'MANDAWA', 'MANESAR', 'MARARRI', 'MANDORMONI', 'MANGALORE', 'MANMAD', 'MARCHULA', 'MATHERAN',
                 'MATHURA', 'MCLEODGANJ', 'MOHALI', 'MOUNT ABU', 'MORADABAD', 'MORBI', 'MUKTESHWAR', 'MUMBAI', 'MUNDRA',
                 'MUNNAR', 'MURUD JANJIRA', 'MUSSOORIE', 'MYSORE', 'NADUKANI', 'NAGAPATTINAM', 'NAGARHOLE',
                 'NAGAUR FORT', 'NAGOTHANE', 'NAGPUR', 'NAHAN', 'NAINITAL', 'NALDHERA', 'NANDED', 'NAPNE', 'NASIK',
                 'NAVI MUMBAI', 'NERAL', 'NEW DELHI', 'NILGIRI', 'NOIDA', 'OOTY', 'ORCHHA', 'OSIAN', 'PACHMARHI',
                 'PALAMPUR', 'PALANPUR', 'PALI', 'PAHALGAM', 'PALITANA', 'PALLAKAD', 'PANCHGANI', 'PANCHKULA', 'PANNA',
                 'PANHALA', 'PANVEL', 'PANTNAGAR', 'PARWANOO', 'PATIALA', 'PATHANKOT', 'PATNA', 'PATNITOP', 'PELLING',
                 'PENCH', 'PHAGWARA', 'PHALODI', 'PINJORE', 'PONDICHERRY', 'POOVAR', 'PORBANDAR', 'PORT BLAIR',
                 'POSHINA', 'PRAGPUR', 'PUNE', 'PURI', 'PUSKHAR', 'PUTTAPARTHI', 'RAI BAREILLY', 'RAICHAK', 'RAIPUR',
                 'RAJASTHAN', 'RAJGIR', 'RAJKOT', 'RAJPIPLA', 'RAJSAMAND', 'RAJAHMUNDRY', 'RAMESHWARAM', 'RAM NAGAR',
                 'RAMGARH', 'RANAKPUR', 'RANCHI', 'RANIKHET', 'RANNY', 'RANTHAMBORE', 'RATNAGIRI', 'RAVANGLA',
                 'RISHIKESH', 'RISHYAP', 'ROHETGARH', 'ROURKELA', 'SAJAN', 'SALEM', 'SAPUTARA', 'SASAN GIR', 'SATTAL',
                 'SAWAI MADHOPUR', 'SAWANTWADI', 'SECUNDERABAD', 'SHILLONG', 'SHIMLA', 'SHIMLIPAL', 'SHIRDI',
                 'SHARAVANBELGOLA', 'SHIVANASAMUDRA', 'SIANA', 'SILIGURI', 'SILVASSA', 'SIVAGANGA DISTRICT', 'SOLAN',
                 'SONAULI', 'SRINAGAR', 'SUNDERBAN', 'SURAT', 'TANJORE', 'TAPOLA', 'TARAPITH', 'THANE', 'THEKKADY',
                 'THIRVANNAMALAI', 'THIRUVANANTHAPURAM', 'TIRUCHIRAPALLI', 'TIRUPUR', 'TIRUPATI', 'THRISSUR', 'UDAIPUR',
                 'UDHAMPUR', 'UDUPI', 'UJJAIN', 'UTTARKASHI', 'VADODARA', 'VAGAMON', 'VARKALA', 'VAPI', 'VARANASI',
                 'VELANKANNI', 'VELLORE', 'VERAVAL', 'VIJAYAWADA', 'VIKRAMGADH', 'VISHAKAPATNAM', 'WAYANAD', 'WANKANER',
                 'YAMUNOTRI', 'YERCAUD', 'YUKSOM']
            for i in alllocations:
                for j in s:
                    if j in i:
                        locations.append(j)
            from collections import Counter

            newlc = locations
            newlc = list(dict.fromkeys(newlc))
            print(newlc)
            ba1 = dict(Counter(locations))
            bz = list(ba1.values())
            counted = []
            for j in bz:
                counted.append(str(j))
            openingsv = counted
            # avarage salary for a search jobtitle
            minsal = 0
            maxsal = 0
            count = 0
            queryset = Jobs.objects.filter(
                Q(jobtitle__icontains=infosearchtitle) | Q(jobdescription__icontains=infosearchtitle)).order_by(
                '-minsal')
            for i in queryset:
                count += 1
                minsal = minsal + int(i.minsal)
                maxsal = maxsal + int(i.maxsal)
            try:
                minsal = int(int(minsal) / count)
                maxsal = int(int(maxsal) / count)
            except:
                minsal = 0
                maxsal = 0
            request.session['minsal'] = str(minsal)
            request.session['maxsal'] = str(minsal)
            request.session['labels'] = (labels)
            request.session['data'] = (data)
            request.session['companies'] = (companies)
            request.session['data'] = (data)

        return render(request, 'pie_chart2.html', {
            'infosearchform': infosearchform,
            'labels': labels,
            'data': data,
            'minsal': minsal,
            'maxsal': maxsal,
            'companies': companies,
            'openings': openings,
            'locations': newlc,
            'openingsloc': openingsv,
        })
    else:
        infosearchform = InfoSearchForm(request.POST)
        return render(request, 'pie_chart2.html', {'infosearchform': infosearchform, 'labels': labels,
                                                   'data': data,
                                                   'minsal': minsal,
                                                   'maxsal': maxsal, })


def searchresults(request):
    searchedtitle = request.session.get('jobtitle')
    searchedminsalary = request.session.get('searchedminsalary')
    searchedminsalary = int(searchedminsalary)
    searchedmaxsalary = request.session.get('searchedmaxsalary')
    searchedmaxsalary = int(searchedmaxsalary)
    searcheddateposted = request.session.get('searcheddateposted')
    searchedcompanyname = request.session.get('searchedcompanyname')
    searchedskills = request.session.get('searchedskills')
    searchedexperience = request.session.get('searchedexperience')
    searchedexperience = int(searchedexperience)
    searchedlocation = request.session.get('searchedlocation')
    searchedjobtype = request.session.get('searchedjobtype')

    enddate = searcheddateposted
    print(enddate)
    startdate = dt.date.today()
    print(startdate)

    # if searchedtitle=="":
    #     searchedtitle=""
    # if searcheddateposted=="":
    #     searcheddateposted=""
    # if searchedjobtype=="":
    #     searchedtitle=""
    # if  searchedlocation=="":
    #     searchedlocation=""
    # if  searchedcompanyname=="":
    #     searchedcompanyname=""
    # if  searchedminsalary=="":
    #     searchedminsalary=100000
    # if  searchedexperience=="":
    #     searchedexperience=1
    # if  searchedskills=="":
    #     searchedskills=""

    if searchedtitle == "":
        searchedtitle = ""
    if searcheddateposted == "":
        searcheddateposted = ""
    if searchedjobtype == "":
        searchedtitle = ""
    if searchedlocation == "":
        searchedlocation = ""
    if searchedcompanyname == "":
        searchedcompanyname = ""
    if searchedminsalary == "":
        searchedminsalary = 100000
    if searchedexperience == "":
        searchedexperience = 1
    if searchedskills == "":
        searchedskills = ""

    print(searchedtitle)
    print(searchedexperience)
    print(searchedjobtype)
    print(searchedskills)
    print(searchedcompanyname)
    print(searchedlocation)
    print(searcheddateposted)
    print(searchedminsalary)
    print(searchedmaxsalary)
    jobsearchform = JobsSearchForm(data=request.POST, instance=request.user)
    # JobsSearchForm()

    from django.db.models import Q
    query = Q()
    if searchedtitle:
        query |= Q(jobtitle__icontains=searchedtitle)
        query |= Q(jobdescription__icontains=searchedtitle)
    print(str(query))
    ##

    # print(q3.query)
    ##    if searchedskills:
    ##        query |= Q(skills__icontains=searchedskills)
    ##    if searchedexperience:
    ##        query &= Q(maxexp__lte=searchedexperience)
    ##        query &= Q(maxexp__gte=searchedexperience)

    # print(query)
    paginator = Paginator(Jobs.objects.filter(query).order_by('-minsal'), 10)

    # paginator = Paginator(Jobs.objects.filter(Q(jobtitle__unaccent__icontains=searchedtitle)|Q(jobdescription__unaccent__icontains=searchedtitle)), 10)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    r = request.user.id
    print(r)
    t = UserProfile.objects.get(id=r)
    lista = t.savedjobs

    li = list(lista.split(','))
    print(li)
    for p in range(0, len(li)):
        if li[p] == '0':
            li.pop(p)
    print(li)
    finalsaved = []
    if li:
        for i in li:
            if not i == "":
                if not i == ',':
                    finalsaved.append(i)
    print(finalsaved)
    for i in range(0, len(finalsaved)):
        finalsaved[i] = int(finalsaved[i])
    context = {
        'finalsaved': finalsaved,
        'users': users,
        'user': request.user,
        'jobsearchform': jobsearchform,
    }
    print("hii1312")
    return render(request, template_name='searchresults.html', context=context)


@login_required(login_url="/login/")
def specificjob(request, id):
    job = Jobs.objects.get(id=id)
    jobtitle = job.jobtitle
    id = job.id
    companyname = job.companyname
    minsal = job.minsal
    maxsal = job.maxsal
    date = job.date
    minexp = job.minexp
    maxexp = job.maxexp
    location = job.location
    jobdescription = job.jobdescription
    jobqualification = job.qualification
    url = job.url
    context = {'url': url, 'id': id, 'companyname': companyname, 'location': location, 'minexp': minexp,
               'maxexp': maxexp,
               'minsal': minsal, 'maxsal': maxsal, 'date': date, 'jobtitle': jobtitle, 'jobdescription': jobdescription,
               'qualification': jobqualification,
               'user': request.user, }
    return render(request, template_name="specificjob.html", context=context)


@login_required(login_url="/login/")
def savedjobs(request, id, id2):
    id = id2
    print("helo")
    c = request.user.profile.user_id
    t = UserProfile.objects.get(id=c)
    b = t.savedjobs
    d = b
    if str(id) in b:
        print("hi")
        return HttpResponseRedirect(reverse('getsavedjobs'))
    t.savedjobs = str(b) + "," + str(id)
    t.save()
    print(t.savedjobs)
    return HttpResponseRedirect(reverse('getsavedjobs'))


@login_required(login_url="/login/")
def delete(request, id):
    r = request.user.id
    print(r)
    t = UserProfile.objects.get(id=r)
    lista = t.savedjobs
    li = list(lista.split(","))
    # li = li[1:]
    ni = []
    print("before")
    print(li)
    print(type(li))
    print(len(li) - 1)
    t = UserProfile.objects.get(id=r)
    p = id
    j = ""
    for i in range(0, len(li)):
        if not str(p) in li[i]:
            t = UserProfile.objects.get(id=r)
            j = j + ',' + str(li[i])
        t.savedjobs = j
        t.save()
    print("final list")
    print(li)
    return HttpResponseRedirect(reverse('getsavedjobs'))


@login_required(login_url="/login/")
def getsavedjobs(request):
    r = request.user.id
    print(r)
    t = UserProfile.objects.get(id=r)
    savedjobssearch = SavedJobsSearch(request.POST)
    lista = t.savedjobs
    # lista=list(lista)
    print("listaaaaa")
    print(lista)
    # lista=lista.replace(',','')
    users = ""
    if request.method == "POST":
        print("after post")
        li = list(lista.split(','))
        print(li)
        for p in range(0, len(li)):
            if li[p] == '0':
                li.pop(p)
        print(li)
        if li:
            for i in li:
                if not i == "":
                    if not i == ',':
                        savedjobssearch.save(commit=False)
                        # job = Jobs.objects.get(id=int(i))
                        ssjobtitile = savedjobssearch.cleaned_data.get('Jobtitle')
                        sssortby = savedjobssearch.cleaned_data.get('Sortby')
                        if sssortby == 'DATE':
                            obj = Jobs.objects.filter(Q(jobtitle__icontains=ssjobtitile) & Q(id=int(i))).order_by(
                                '-date')
                            paginator = Paginator(obj, 5)
                        if sssortby == 'SALARY':
                            obj = Jobs.objects.filter(Q(jobtitle__icontains=ssjobtitile) & Q(id=int(i))).order_by(
                                '-maxsal')
                            paginator = Paginator(obj, 5)
                        if sssortby == 'EXPERIENCE':
                            obj = Jobs.objects.filter(Q(jobtitle__icontains=ssjobtitile) & Q(id=int(i))).order_by(
                                '-minexp')
                            paginator = Paginator(obj, 5)

                        page = request.GET.get('page', 1)
                        try:
                            users = paginator.page(page)
                        except PageNotAnInteger:
                            users = paginator.page(1)
                        except EmptyPage:
                            users = paginator.page(paginator.num_pages)
                    else:
                        b = "No jobs"
        context = {
            'users': users,
            'user': request.user,
            'savedjobssearch': savedjobssearch,
        }
        print("hii1312")
        return render(request, template_name='saved.html', context=context)
    else:
        # lista=lista.replace(',','')
        li = list(lista.split(','))
        for p in range(0, len(li)):
            if li[p] == '0':
                li.pop(p)
        print("else part")

        print(li)
        if li:
            jobtitle = []
            minsal = []
            minexp = []
            maxsal = []
            maxexp = []
            location = []
            companyname = []
            jobid = []
            date = []
            skills = []
            jobportal = []
            jobtype = []
            urls = []
            degree = []
            for i in li:
                if not i == "":
                    if not i == ',':
                        job = Jobs.objects.get(id=int(i))
                        urls.append(job.url)
                        skills.append(job.skills)
                        jobportal.append(job.jobportal)
                        jobtype.append(job.jobtype)
                        jobtitle.append(job.jobtitle)
                        companyname.append(job.companyname)
                        minsal.append(job.minsal)
                        maxsal.append(job.maxsal)
                        minexp.append(job.minexp)
                        maxexp.append(job.maxexp)
                        date.append(job.date)
                        location.append(job.location)
                        jobid.append(job.id)
                        degree.append(job.qualification)
                    else:
                        b = "No jobs"
            count = len(jobtitle)
            context = {
                'savedjobssearch': savedjobssearch,
                'count': range(0, count),
                'user': request.user,
                'zipe2': zip(companyname, skills, jobportal, jobtype, urls, jobtitle, maxsal, minsal, maxexp, minexp,
                             location, date, jobid, degree)
            }
            return render(request, template_name="saved.html", context=context)


p = ""
global s1
global s2
global s3
global s4
global s5
global s6
global s7
global s8
global s9


@login_required(login_url="/login/")
def JobsForYou(request):
    r = request.user.id
    print(r)
    user = UserProfile.objects.get(id=r)
    print(user)
    skills = user.skills
    print(skills)
    city = user.city

    paginator = Paginator(
        Jobs.objects.filter(Q(jobtitle__icontains=skills, location__icontains=city)), 10)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    lista = user.savedjobs

    li = list(lista.split(','))
    print(li)
    for p in range(0, len(li)):
        if li[p] == '0':
            li.pop(p)
    print(li)
    finalsaved = []
    if li:
        for i in li:
            if not i == "":
                if not i == ',':
                    finalsaved.append(i)
    print(finalsaved)
    for i in range(0, len(finalsaved)):
        finalsaved[i] = int(finalsaved[i])

    context = {
        'finalsaved': finalsaved,
        'users': users,
        'user': request.user,
        # 'jobsearchform': jobsearchform,
    }
    return render(request, template_name='jobsforyou.html', context=context)


@login_required(login_url="/login/")
def result(request):
    if request.method == 'POST':
        context = {}
        jobsearchform = JobsSearchForm(request.POST, instance=request.user)
        print("before search")
        print("after search")
        if jobsearchform.is_valid():
            print("inside uform")
            jobsearchform.save()
        searchedsalary = jobsearchform.cleaned_data.get('salary')

        print(searchedsalary)
        if searchedsalary == '1to3Lacs':
            searchedminsalary = 100000
            searchedmaxsalary = 300000
        elif searchedsalary == '3to5lacs':
            searchedminsalary = 300000
            searchedmaxsalary = 500000
        elif searchedsalary == '5to7lacs':
            searchedminsalary = 500000
            searchedmaxsalary = 700000
        elif searchedsalary == '7to9lacs':
            searchedminsalary = 700000
            searchedmaxsalary = 900000
        elif searchedsalary == '9to11lacs':
            searchedminsalary = 900000
            searchedmaxsalary = 1100000
        else:
            searchedminsalary = 100000
            searchedmaxsalary = 300000

        searcheddateposted = str(jobsearchform.cleaned_data.get('dateposted'))

        searchedtitle = str(jobsearchform.cleaned_data.get('jobtitle'))
        Temp.objects.create(searchedtitle=searchedtitle)
        print(searchedtitle)
        jsf = searchedtitle
        try:
            searchedexperience = int(jobsearchform.cleaned_data.get('experience'))
        except:
            searchedexperience = 1
        searcheddatetoday = dt.datetime.today()
        if searcheddateposted == 'Within1day':
            date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        elif searcheddateposted == 'Within1week':
            date = datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d')
        elif searcheddateposted == 'Within15days':
            date = datetime.strftime(datetime.now() - timedelta(15), '%Y-%m-%d')
        elif searcheddateposted == 'WithinAMonth':
            date = datetime.strftime(datetime.now() - timedelta(30), '%Y-%m-%d')
        else:
            date = datetime.strftime(datetime.now() - timedelta(182), '%Y-%m-%d')
        searcheddateposted2 = date

        searchedlocation = jobsearchform.cleaned_data.get('location')
        if searchedlocation == "":
            searchedlocation = "india"
        searchedcompanyname = jobsearchform.cleaned_data.get('companyname')
        searchednoofjobs = jobsearchform.cleaned_data.get('noofjobs')
        searchedjobtype = jobsearchform.cleaned_data.get('jobtype')

        if searchedjobtype == "FULL-TIME":
            searchedjobtype = "FULL-TIME"
            jobtypeshine = "1"
        elif searchedjobtype == "PART-TIME":
            searchedjobtype = "PART-TIME"
            jobtypeshine = "2"
        elif searchedjobtype == "INTERNSHIP":
            searchedjobtype = "INTERNSHIP"
            jobtypeshine = "3"
        elif searchedjobtype == "WORK-FROM-HOME":
            searchedjobtype = "WORK-FROM-HOME"
            jobtypeshine = "4"
        else:
            jobtypeval = "FULL-TIME"
            jobtypeshine = "1"

        searchedskills = jobsearchform.cleaned_data.get('skills')
        date_time_str = searcheddateposted2
        searcheddateposted = datetime.strptime(date_time_str, '%Y-%m-%d').date()
        b = indeedsearch(searchedminsalary, searchedmaxsalary, searcheddateposted, searchedsalary, searchedcompanyname,
                         searchedskills, searchedlocation, searchedexperience, searchedtitle, searchednoofjobs,
                         searchedjobtype)
        request.session['jobtitle'] = str(searchedtitle)
        request.session['searchedminsalary'] = str(searchedminsalary)
        request.session['searchedmaxsalary'] = str(searchedmaxsalary)
        request.session['searcheddateposted'] = str(searcheddateposted)
        request.session['searchedcompanyname'] = str(searchedcompanyname)
        request.session['searchedskills'] = str(searchedskills)
        request.session['searchedexperience'] = str(searchedexperience)
        request.session['searchedlocation'] = str(searchedlocation)
        request.session['searchedjobtype'] = str(searchedjobtype)

        return HttpResponseRedirect(reverse('searchresults'))
    # return searchresults(request, searchedtitle, searcheddateposted, searchedskills, searchedmaxsalary,
    #                     searchedminsalary, searchedexperience, searchedcompanyname, searchedlocation, searchedjobtype)
    else:
        return HttpResponseRedirect(reverse('searchresults'))


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('search'))
    else:
        return render(request, "index.html")


def register(request):
    form = RegistrationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            print("form is valid")
            # user = form.save(commit=False)
            user = form.save(commit=True)
            user.is_active = True
            user.save()
            print("current1")
            current_site = get_current_site(request)
            print("current2")
            print(current_site)
            mail_subject = 'Activate your account.'
            message = render_to_string('account_activation_email.html', {
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
            messages.success(request, ('Please Confirm your email to complete registration.'))
            return HttpResponseRedirect(reverse('login'))
        else:
            print("else1")
            form = RegistrationForm(request.POST)
            return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.profile.email_confirmed = 1
        user.is_active = True
        user.save()
        #   login(request)
        # return redirect('home')
        messages.success(request, ('Your account have been confirmed.'))
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    context = {}
    if request.method == "POST":
        loginvar = LoginForm(request.POST)
        if loginvar.is_valid():
            username = request.POST['username']
            print(username)
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                if user.profile.email_confirmed == 0:
                    messages.success(request, ('Please Confirm your email first.'))
                    return HttpResponseRedirect(reverse('login'))
                if user.profile.email_confirmed == 1:
                    if user.is_active:
                        auth.login(request, user)
                        print("you are now logined")

                        return HttpResponseRedirect(reverse('search'))
                    else:
                        print("User not active")
                        context['err'] = "User not active"
                        return render(request, 'login.html', context=context)

            else:
                loginvar = LoginForm()
                print("Provide valid 2credentials")
                # err = "Provide valid credentials"
                messages.error(request, 'Invalid Login Credentials, Please Try Again')
                return render(request, 'login.html', context={"form": loginvar, "hello": 3})
    else:
        print("else block")
        loginvar = LoginForm()
        return render(request=request, template_name="login.html", context={"form": loginvar, "hello": 3})


@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    print("logged out")
    context = {}
    context['msg'] = "you hav been loggedout login again"
    return render(request=request, template_name="logout.html", context=context)


@login_required(login_url="/login/")
def ProfileView(request):
    if request.method == "POST":
        print("before uform")
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        print("befor form")
        if u_form.is_valid() and p_form.is_valid():
            print("inside uform")

            # Example = modelformset_factory(model=Example2, fields=('name', 'location'))
            # if request.method == "POST":
            #     form = Example(request.POST)
            #     instance = form.save()
            # form = Example()
            # context = {'form': form}
            # return render(request, template_name='example.html', context=context)

            u_form.save()
            p_form.save()
            jobsearchform = JobsSearchForm(request.POST, instance=request.user)
            context = {
                'jobsearchform': jobsearchform,
            }
            return render(request, template_name="search.html", context=context)
        else:
            print("da")
            jobsearchform = JobsSearchForm()
            context = {
                'jobsearchform': jobsearchform,
            }
            return render(request, template_name="search.html", context=context)
    else:
        print("http rsponse error in else")
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, template_name="profile/profile.html", context=context)


class AuthRequiredMiddleware(object):
    def process_request(self, request):
        redirect_url = '/admin/login'

        if not request.user.is_authenticated() and request.path != redirect_url:
            return HttpResponseRedirect(redirect_url)
        return None


@login_required(login_url="/login/")
def JobSearchView(request):
    if request.method == "POST":
        print("before search")
        jobsearchform = JobsSearchForm(request.POST, instance=request.user)

        print("after search")
        if jobsearchform.is_valid():
            print("inside uform")
            print("http rsponse error in else")
            return render(request, template_name="search.html")
    else:
        print("http rsponse error in else")
        jobsearchform = JobsSearchForm(instance=request.user)
        context = {
            'jobsearchform': jobsearchform,
        }
        return render(request, template_name="search.html", context=context)

