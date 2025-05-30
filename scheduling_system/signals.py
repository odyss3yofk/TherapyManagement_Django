from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import Therapist, TherapistAttendance


@receiver(user_logged_in)
def mark_therapist_attendance(sender, user, request, **kwargs):
    try:
        therapist = Therapist.objects.get(user=user)
    except Therapist.DoesNotExist:
        return  # Not a therapist, ignore

    now = timezone.localtime()
    attendance_time = now.time()
    if attendance_time >= timezone.datetime.strptime('17:00', '%H:%M').time() and \
       attendance_time <= timezone.datetime.strptime('17:30', '%H:%M').time():
        # Mark attendance only if not already marked today
        attendance, created = TherapistAttendance.objects.get_or_create(
            therapist=therapist,
            date=now.date(),
            defaults={'present': True}
        )
