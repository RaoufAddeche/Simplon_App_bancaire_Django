from django.urls import path
from user.views import (
    HomeView,
    UserRegistrationView,
    UserLoginView,
    ClientDashboardView,
    AdvisorDashboardView
)
from django.contrib.auth.views import LogoutView
from django.urls import include, path


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('client/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('advisor/', AdvisorDashboardView.as_view(), name='advisor_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
