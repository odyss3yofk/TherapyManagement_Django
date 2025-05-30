from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Therapist, Parent, Child, TherapySession, TherapistAttendance


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


class TherapistAttendanceAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'date', 'present', 'timestamp')
    list_filter = ('present', 'date', 'therapist')
    search_fields = ('therapist__user__username',
                     'therapist__user__first_name', 'therapist__user__last_name')
    date_hierarchy = 'date'
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=attendance.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected as CSV"

    def changelist_view(self, request, extra_context=None):

        total = TherapistAttendance.objects.count()
        present = TherapistAttendance.objects.filter(present=True).count()
        absent = total - present
        extra_context = extra_context or {}
        extra_context['attendance_summary'] = {
            'total': total,
            'present': present,
            'absent': absent,
        }
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(TherapistAttendance, TherapistAttendanceAdmin)
