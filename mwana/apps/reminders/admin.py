from django.contrib import admin
from django import forms
from django.db import models

from mwana.apps.reminders import models as reminders


class AppointmentInline(admin.TabularInline):
    model = reminders.Appointment


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    inlines = (AppointmentInline,)
    list_select_related = True
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug',)
admin.site.register(reminders.Event, EventAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'num_days',)
    list_filter = ('event',)
    list_select_related = True
    search_fields = ('name', 'event__name',)
admin.site.register(reminders.Appointment, AppointmentAdmin)


class PatientEventAdmin(admin.ModelAdmin):
    list_display = ('patient', 'event', 'date','date_logged','cba_conn',)
    list_filter = ('event','date_logged',)
    date_hierarchy = 'date_logged'
admin.site.register(reminders.PatientEvent, PatientEventAdmin)


class SentNotificationInline(admin.TabularInline):
    model = reminders.SentNotification


class SentNotificationAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'patient_event', 'recipient', 'date_logged',)
    list_filter = ('appointment', 'date_logged',)
    list_select_related = True
    search_fields = ('appointment__name', 'patient__name', 'recipient__name',
                     'recipient__alias',)
admin.site.register(reminders.SentNotification, SentNotificationAdmin)

