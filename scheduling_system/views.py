from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import TherapistRegistrationForm, ParentRegistrationForm, TherapistEditForm
from .models import Therapist, Parent, Child


def index(request):
    return render(request, 'scheduling_system/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Therapist').exists():
                return redirect('therapist_dashboard')
            elif user.groups.filter(name='Parent').exists():
                return redirect('parent_dashboard')
            else:
                return redirect('index')
        else:
            return render(request, 'scheduling_system/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'scheduling_system/login.html')


def logout_view(request):
    logout(request)
    return redirect('login_view')  # or your login page's URL name


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_therapist(user):
    return user.groups.filter(name='Therapist').exists()


def is_parent(user):
    return user.groups.filter(name='Parent').exists()


# --------------------------
# Dashboards (optional for now)
# --------------------------

# @login_required
# @user_passes_test(is_admin)
# def admin_dashboard(request):
#     return render(request, 'scheduling_system/admin_dashboard.html')

@login_required
@user_passes_test(is_therapist)
def therapist_dashboard(request):
    try:
        therapist = Therapist.objects.get(user=request.user)
    except Therapist.DoesNotExist:
        return redirect('login_view')

    edit_mode = request.GET.get('edit') == 'true'

    if request.method == 'POST':
        form = TherapistEditForm(request.POST, instance=therapist)
        if form.is_valid():
            form.save()
            return redirect('therapist_dashboard')
    else:
        form = TherapistEditForm(instance=therapist)

    return render(request, 'scheduling_system/therapist_dashboard.html', {
        'form': form,
        'therapist': therapist,
        'edit_mode': edit_mode
    })

# @login_required
# @user_passes_test(is_parent)
# def parent_dashboard(request):
#     return render(request, 'scheduling_system/parent_dashboard.html')


def register_therapist(request):
    if request.method == 'POST':
        form = TherapistRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.first_name = form.cleaned_data['name']
            user.save()

            group, _ = Group.objects.get_or_create(name='Therapist')
            user.groups.add(group)

            Therapist.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                specialization=form.cleaned_data['specialization'],
                experience_years=form.cleaned_data['experience_years'],

            )

            return redirect('login_view')
    else:
        form = TherapistRegistrationForm()

    return render(request, 'scheduling_system/register_therapist.html', {'form': form})


def register_parents(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                return render(request, 'scheduling_system/register_parents.html', {
                    'form': form,
                    'error': "Passwords do not match."
                })

            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            group, _ = Group.objects.get_or_create(name='Parent')
            user.groups.add(group)

            parent = Parent.objects.create(
                name=form.cleaned_data['name'],
                user=user,
                phone_number=form.cleaned_data['phone_number']
            )

            # Create child
            Child.objects.create(
                parent=parent,
                name=form.cleaned_data['child_name'],
                age=form.cleaned_data['child_age'],
                diagnosis=form.cleaned_data['child_diagnosis']
            )

            login(request, user)
            return redirect('parent_dashboard')
    else:
        form = ParentRegistrationForm()

    return render(request, 'scheduling_system/register_parents.html', {'form': form})


@login_required
@user_passes_test(is_therapist)
def profile(request):
    therapist = Therapist.objects.get(user=request.user)
    return render(request, 'scheduling_system/therapist_dashboard.html', {'therapist': therapist})
