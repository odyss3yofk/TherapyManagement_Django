from django.db import models
from django.contrib.auth.models import User


class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    available_morning = models.BooleanField(default=True)
    available_afternoon = models.BooleanField(default=True)
    available_evening = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    diagnosis = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TherapySession(models.Model):
    therapist = models.ForeignKey(
        Therapist,
        on_delete=models.CASCADE,
        related_name='therapy_sessions'
    )
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.child.name} with {self.therapist.user.username} on {self.date}"


class TherapistAttendance(models.Model):
    therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('therapist', 'date')

    def __str__(self):
        return f"{self.therapist.user.username} - {self.date} - {'Present' if self.present else 'Absent'}"
