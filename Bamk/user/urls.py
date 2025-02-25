from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('activate/<str:email>/', views.activate_account_view, name='activate_account'),
]