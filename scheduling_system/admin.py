from django.contrib import admin
from .models import Therapist, Parent, Child, TherapySession


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone_number')
    search_fields = ('user__username', 'specialization', 'phone_number')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'age', 'diagnosis')
    search_fields = ('name', 'diagnosis', 'parent__user__username')
    list_filter = ('age',)


@admin.register(TherapySession)
class TherapySessionAdmin(admin.ModelAdmin):
    list_display = ('child', 'therapist', 'date', 'time', 'duration_minutes')
    search_fields = ('child__name', 'therapist__user__username', 'notes')
    list_filter = ('date', 'therapist')
    date_hierarchy = 'date'
