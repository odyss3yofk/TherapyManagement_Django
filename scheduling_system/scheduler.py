from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus
from django.utils import timezone
from .models import Therapist, Child, TherapySession, TherapistAttendance
from datetime import timedelta


def run_scheduler():
    today = timezone.localtime().date()
    print("Scheduler running for date:", today)

    therapists = list(
        Therapist.objects.filter(
            therapistattendance__date=today,
            therapistattendance__present=True
        ).distinct()
    )
    children = list(Child.objects.all())
    sessions = ["Morning", "Afternoon", "Evening"]
    courses = ["Speech", "Occupational", "Behavioral"]

    session_times = {
        "Morning": timezone.datetime.strptime("10:00", "%H:%M").time(),
        "Afternoon": timezone.datetime.strptime("14:00", "%H:%M").time(),
        "Evening": timezone.datetime.strptime("17:00", "%H:%M").time(),
    }

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

    # Decision variables: x[(t.id, s, c, child.id)] = 1 if therapist t assigned to child for course c in session s
    x = {}
    for t in therapists:
        for s in sessions:
            for c in courses:
                for child in children:
                    x[(t.id, s, c, child.id)] = LpVariable(
                        f"x_{t.id}_{s}_{c}_{child.id}", cat="Binary"
                    )

    # Objective: maximize total assignments
    model += lpSum(
        x[(t.id, s, c, child.id)]
        for t in therapists for s in sessions for c in courses for child in children
    )

    # Each child can be assigned to at most one therapist per session and course
    for s in sessions:
        for c in courses:
            for child in children:
                model += lpSum(x[(t.id, s, c, child.id)] for t in therapists) <= 1

    # Each therapist can handle only one child per session and course
    for t in therapists:
        for s in sessions:
            for c in courses:
                model += lpSum(x[(t.id, s, c, child.id)] for child in children) <= 1

    # Therapist availability constraint (max 3 courses per session)
    for t in therapists:
        for s in sessions:
            model += lpSum(x[(t.id, s, c, child.id)] for c in courses for child in children) <= availability.get((t.id, s), 0) * 3

    # Each child can have at most 3 courses per session
    for s in sessions:
        for child in children:
            model += lpSum(x[(t.id, s, c, child.id)] for t in therapists for c in courses) <= 3

    print("Therapists:", therapists)
    print("Children:", children)
    print("Availability:", availability)
    model.solve()
    print(f"Status: {LpStatus[model.status]}")

    # Define the order of courses for time calculation
    course_order = ["Speech", "Occupational", "Behavioral"]
    course_duration = 40  # minutes
    course_gap = 15       # minutes

    TherapySession.objects.all().delete()
    for s in sessions:
        session_start = session_times[s]
        for idx, c in enumerate(course_order):
            # Calculate the start time for this course in the session
            start_minutes = idx * (course_duration + course_gap)
            # Convert session_start to datetime for addition
            session_datetime = timezone.datetime.combine(today, session_start)
            course_start_time = (session_datetime + timedelta(minutes=start_minutes)).time()
            for child in children:
                for t in therapists:
                    key = (t.id, s, c, child.id)
                    if x[key].varValue == 1:
                        TherapySession.objects.create(
                            therapist=t,
                            child=child,
                            date=today,
                            time=course_start_time,
                            duration_minutes=course_duration,
                            notes=f"Assigned to {c} in {s} session"
                        )
