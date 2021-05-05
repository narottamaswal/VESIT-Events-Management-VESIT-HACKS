from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls import static
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView
from . import views
urlpatterns = [
    path('asas',views.assa,name='asas'),
    path('register/', views.register, name="register"),
    path('createaevent',views.createEvent,name='createaevent'),
path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    #   path('', views.homepage, name="homepage"),
    path('events/', views.EventHomepage, name="ehomepage"),
    path('myevents/',views.myRegisteredEvents,name='myRegisteredEvents'),
    path('event/<int:id>',views.eventDetail,name='eventDetail'),
    path('event/<int:id>/register', views.eventRegister, name='eventRegister'),
    path('event/approve',views.EventForApproval,name='eventapprovalpage'),
    path('event/<int:id>/approved',views.approve,name='eventapprove')
    # path('logout', logout, name="logout"),
    # path('resume', resume, name="resume"),
    # path('profile', ProfileView, name="profile"),
    # path('result', result, name="result"),
    # path('search', JobSearchView, name="search"),
    # path('example', example, name="example"),
    # path('specificjob/<int:id>/', specificjob, name='specificjob'),
    # path('demo', demo, name='demo'),
    # path('info', info, name='info'),
    # path('resumepdf',pdfview,name='resumepdf'),
    # path('jobsforyou', JobsForYou, name='JobsForYou'),
    # path('searchresults', searchresults, name='searchresults'),
    # path('delete-<int:id>', delete, name='delete'),
    # path('createyourresume', createyourresume, name='createyourresume'),
    # path('resumegenerator', resumegenerator, name='resumegenerators'),
    # path('getsavedjobs', getsavedjobs, name="getsavedjobs"),
    # path('specificjob/<int:id>/savedjobs/<int:id2>', savedjobs, name='savedjobs'),
    # path('',index,name="index"),
    # path('change-password', PasswordChangeView.as_view(template_name='PasswordChangeAndReset/password_change_form.html',success_url='/'), name='change-password'),
    #
    #
    # path('password-reset/',PasswordResetView.as_view(template_name='PasswordChangeAndReset/password_reset_form.html',
    #          subject_template_name='PasswordChangeAndReset/password_reset_subject.txt',
    #          email_template_name='PasswordChangeAndReset/password_reset_email.html',
    #          # success_url='/login/'
    #      ),
    #      name='password_reset'),
    # path('password-reset/done/',
    #    PasswordResetDoneView.as_view(
    #          template_name='PasswordChangeAndReset/password_reset_done.html'
    #      ),
    #      name='password_reset_done'),
    # path('password-reset-confirmation/<uidb64>/<token>/',
    #     PasswordResetConfirmView.as_view(
    #          template_name='PasswordChangeAndReset/password_reset_confirmation.html'
    #      ),
    #      name='password_reset_confirmation'),
    # path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='PasswordChangeAndResetpassword/password_reset_complete.html'
    #      ),
    #      name='password_reset_complete'),
]
