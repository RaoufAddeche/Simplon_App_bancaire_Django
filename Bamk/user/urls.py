from django.urls import path
from user.views import (
    HomeView,
    UserRegistrationView,
    UserLoginView,
    ClientDashboardView,
    AdvisorDashboardView,
    ListClientView,
    ClientFileView,
)
from django.contrib.auth.views import LogoutView
from django.urls import include, path

app_name = 'user'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('client/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('advisor/', AdvisorDashboardView.as_view(), name='advisor_dashboard'),
    path('list_client/', ListClientView.as_view(), name='list_clients'),
    path('client/<int:pk>/file/', ClientFileView.as_view(), name='client_file'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("__reload__/", include("django_browser_reload.urls")),
]
