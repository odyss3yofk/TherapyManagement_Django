from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    availability = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening')
        ],
        default='morning'
    )

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
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.child.name} with {self.therapist.user.username} on {self.date}"
