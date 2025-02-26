# loan/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import LoanRequestForm
from .services import LoanAPIService

@method_decorator(login_required, name='dispatch')
class LoanRequestView(View):
    """Vue pour soumettre une demande de prêt"""
    def get(self, request):
        form = LoanRequestForm()
        return render(request, "loan/loan_request.html", {"form": form})

    def post(self, request):
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            # Soumettre à l'API FastAPI
            result = LoanAPIService.submit_loan_request(request, form.cleaned_data)

            if "error" not in result:
                # Vérifier la prédiction
                if result.get("eligible", False):
                    return redirect("loan_approved")
                else:
                    return redirect("loan_rejected")
            else:
                error_msg = "Erreur lors de la soumission de la demande"
                if result.get("error") == "authentication_error":
                    error_msg = "Erreur d'authentification, veuillez vous reconnecter"
                messages.error(request, error_msg)

        return render(request, "loan/loan_request.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class UserLoansView(View):
    """Vue pour afficher l'historique des prêts"""
    def get(self, request):
        result = LoanAPIService.get_loan_history(request)

        if "error" in result:
            error_msg = "Impossible de récupérer l'historique des prêts"
            if result.get("error") == "authentication_error":
                error_msg = "Erreur d'authentification, veuillez vous reconnecter"
            messages.error(request, error_msg)
            loans = []
        else:
            loans = result

        return render(request, "loan/user_loans.html", {"loans": loans})

@method_decorator(login_required, name='dispatch')
class LoanApprovedView(View):
    """Vue pour afficher la page de prêt approuvé"""
    def get(self, request):
        return render(request, "loan/loan_approved.html")

@method_decorator(login_required, name='dispatch')
class LoanRejectedView(View):
    """Vue pour afficher la page de prêt rejeté"""
    def get(self, request):
        return render(request, "loan/loan_rejected.html")

@method_decorator(login_required, name='dispatch')
class AdvisorLoansView(View):
    """Vue pour les conseillers pour voir les prêts"""
    def get(self, request):
        if not request.user.is_staff:
            messages.error(request, "Accès refusé")
            return redirect("home")

        result = LoanAPIService.get_advisor_loans(request)

        if "error" in result:
            error_msg = "Impossible de récupérer les prêts des clients"
            if result.get("error") == "authentication_error":
                error_msg = "Erreur d'authentification, veuillez vous reconnecter"
            messages.error(request, error_msg)
            client_loans = {}
        else:
            client_loans = result

        return render(request, "loan/advisor_loans.html", {"client_loans": client_loans})