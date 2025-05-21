from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/therapist/', views.register_therapist,
         name='register_therapist'),
    path('register/parents/', views.register_parents, name='register_parents'),
    # path('/logout/', views.logout, name='logout'),
    # path('/dashboard/', views.dashboard, name='dashboard'),



]
