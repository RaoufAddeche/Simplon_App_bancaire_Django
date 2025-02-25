# loan/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.loan_request_view, name='loan_request'),
    path('history/', views.user_loans_view, name='user_loans'),
    path('approved/', views.loan_approved_view, name='loan_approved'),
    path('rejected/', views.loan_rejected_view, name='loan_rejected'),
    path('advisor/', views.loan_approved_view, name='advisor_loan'),
]