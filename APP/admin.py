from django.contrib import admin
from .models import Staff,Student,Roles,CustomUser,Organizer,Event,EventsRegister
# Register your models here.

def download_csv(modeladmin, request, queryset):
    import csv
    f = open('some.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['user', 'dept', 'role_id'])
    for s in queryset:
        writer.writerow([s.user, s.dept, s.role_id])


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','dept','role_id')
    list_editable = ('dept','role_id')
    actions = [download_csv]
    search_fields = ('user',)
    list_filter = ('dept',)

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user','dept','role_id')
    list_editable = ('dept','role_id')
    actions = [download_csv]
    search_fields = ('user',)
    list_filter = ('dept',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title','description','date',)
    actions = [download_csv]




admin.site.register(Staff,StaffAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Roles)
admin.site.register(CustomUser)
admin.site.register(Organizer)
admin.site.register(Event,EventAdmin)
admin.site.register(EventsRegister)

# src/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
