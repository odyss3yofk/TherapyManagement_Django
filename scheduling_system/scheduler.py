from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus
from django.utils import timezone
from .models import Therapist, Child, TherapySession


def run_scheduler():
    # Extract data from models
    therapists = list(Therapist.objects.all())
    children = list(Child.objects.all())

    # Placeholder: extract courses and sessions (extend your models to support these if needed)
    courses = ["Speech", "Occupational", "Behavioral"]  # Example course names
    sessions = ["Morning", "Afternoon", "Evening"]  # Example session labels

    # Therapist availability (you might store this in your DB)
    availability = {}
    for therapist in therapists:
        for session in sessions:
            if session == "Morning":
                availability[(therapist.id, session)] = int(therapist.available_morning)
            elif session == "Afternoon":
                availability[(therapist.id, session)] = int(therapist.available_afternoon)
            elif session == "Evening":
                availability[(therapist.id, session)] = int(therapist.available_evening)

    # Create LP model
    model = LpProblem("Therapy_Scheduling", LpMaximize)

    # Decision variables
    x = {}
    for t in therapists:
        for c in courses:
            for s in sessions:
                for child in children:
                    x[(t.id, c, s, child.id)] = LpVariable(
                        f"x_{t.id}_{c}_{s}_{child.id}", cat="Binary")

    # Objective
    model += lpSum(x[(t.id, c, s, child.id)]
                   for t in therapists for c in courses for s in sessions for child in children)

    # Constraints
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

    # Solve
    model.solve()
    print(f"Status: {LpStatus[model.status]}")

    # Apply results to DB
    TherapySession.objects.all().delete()  # Optional: clear existing
    for s in sessions:
        for c in courses:
            for child in children:
                for t in therapists:
                    key = (t.id, c, s, child.id)
                    if x[key].varValue == 1:
                        TherapySession.objects.create(
                            therapist=t,
                            child=child,
                            date=timezone.now().date(),  # You can set real dates and times here
                            time=timezone.now().time(),
                            duration_minutes=30,
                            notes=f"Assigned to {c} in {s} session"
                        )
