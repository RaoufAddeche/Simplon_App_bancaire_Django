from django.urls import path
from . import views

urlpatterns = [
    path("request/", views.loan_request, name="loan_request"),  # Soumettre une demande de prêt
    path("history/", views.user_loans, name="user_loans"),  # Historique des prêts pour le demandeur
    path("advisor/", views.advisor_loans, name="advisor_loans"),  # Prêts assignés au conseiller
]