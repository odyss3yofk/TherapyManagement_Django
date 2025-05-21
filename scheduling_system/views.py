from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

# Home page


def index(request):
    return render(request, 'scheduling_system/index.html')

# Login view


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on user group
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Therapist').exists():
                return redirect('therapist_dashboard')
            elif user.groups.filter(name='Parent').exists():
                return redirect('parent_dashboard')
            else:
                return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

# Logout view


def logout_view(request):
    logout(request)
    return redirect('login_view')

# Group check functions


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_therapist(user):
    return user.groups.filter(name='Therapist').exists()


def is_parent(user):
    return user.groups.filter(name='Parent').exists()

# Dashboards with access control


# @login_required
# @user_passes_test(is_admin)
# def admin_dashboard(request):
#     return render(request, 'scheduling_system/admin_dashboard.html')


# @login_required
# @user_passes_test(is_therapist)
# def therapist_dashboard(request):
#     return render(request, 'scheduling_system/therapist_dashboard.html')


# @login_required
# @user_passes_test(is_parent)
# def parent_dashboard(request):
#     return render(request, 'scheduling_system/parent_dashboard.html')

# Registration pages (just renders templates for now)


def register_therapist(request):
    return render(request, 'scheduling_system/register_therapist.html')


def register_parents(request):
    return render(request, 'scheduling_system/register_parents.html')
