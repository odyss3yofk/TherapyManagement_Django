from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus
from django.utils import timezone
from .models import Therapist, Child, TherapySession, TherapistAttendance


def run_scheduler():
    today = timezone.now().date()
    # Only include therapists who are present today
    therapists = list(
        Therapist.objects.filter(
            therapistattendance__date=today,
            therapistattendance__present=True
        ).distinct()
    )
    children = list(Child.objects.all())

    courses = ["Speech", "Occupational", "Behavioral"]
    sessions = ["Morning", "Afternoon", "Evening"]

    # Therapist availability (using BooleanFields)
    availability = {}
    for therapist in therapists:
        for session in sessions:
            if session == "Morning":
                availability[(therapist.id, session)] = int(
                    therapist.available_morning)
            elif session == "Afternoon":
                availability[(therapist.id, session)] = int(
                    therapist.available_afternoon)
            elif session == "Evening":
                availability[(therapist.id, session)] = int(
                    therapist.available_evening)

    model = LpProblem("Therapy_Scheduling", LpMaximize)

    x = {}
    for t in therapists:
        for c in courses:
            for s in sessions:
                for child in children:
                    x[(t.id, c, s, child.id)] = LpVariable(
                        f"x_{t.id}_{c}_{s}_{child.id}", cat="Binary"
                    )

    model += lpSum(
        x[(t.id, c, s, child.id)]
        for t in therapists for c in courses for s in sessions for child in children
    )

    for s in sessions:
        for c in courses:
            for child in children:
                model += lpSum(x[(t.id, c, s, child.id)]
                               for t in therapists) == 1

    for t in therapists:
        for c in courses:
            for s in sessions:
                for child in children:
                    model += x[(t.id, c, s, child.id)
                               ] <= availability.get((t.id, s), 0)

    for t in therapists:
        for c in courses:
            for s in sessions:
                model += lpSum(x[(t.id, c, s, child.id)]
                               for child in children) <= 1

    model.solve()
    print(f"Status: {LpStatus[model.status]}")

    TherapySession.objects.all().delete()
    for s in sessions:
        for c in courses:
            for child in children:
                for t in therapists:
                    key = (t.id, c, s, child.id)
                    if x[key].varValue == 1:
                        TherapySession.objects.create(
                            therapist=t,
                            child=child,
                            date=today,
                            time=timezone.now().time(),
                            duration_minutes=30,
                            notes=f"Assigned to {c} in {s} session"
                        )
