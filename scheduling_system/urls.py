from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/therapist/', views.register_therapist,
         name='register_therapist'),
    path('register/parents/', views.register_parents, name='register_parents'),
    path('login/therapist/', views.therapist_dashboard,
         name='therapist_dashboard'),
    path('login/parents/', views.parent_dashboard, name='parent_dashboard'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile, name='profile'),
    path('sessions/', views.sessions, name='sessions'),
    path('profile/sessions', views.profile, name='profile_sessions'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('/dashboard/', views.dashboard, name='dashboard'),



]
