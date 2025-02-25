
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .services import LoanService
from .forms import LoanApplicationForm

@login_required  # Cette décoration assure que l'utilisateur est connecté
def loan_request_view(request):
    """Page de demande de prêt"""
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            # Récupérer le token JWT
            token = request.session.get('jwt_token')
            if not token:
                messages.error(request, "Session expirée. Reconnectez-vous.")
                return redirect('login')

            # Préparer les données du prêt
            loan_data = form.cleaned_data

            # Envoyer la demande
            loan_service = LoanService(token)
            result = loan_service.submit_loan_request(loan_data)

            # Traiter le résultat
            if 'error' not in result:
                if result.get('eligible', False):
                    return redirect('loan_approved')
                else:
                    return redirect('loan_rejected')
            else:
                messages.error(request, "Erreur lors de la demande")
    else:
        form = LoanApplicationForm()

    return render(request, 'loan/loan_request.html', {'form': form})

@login_required
def user_loans_view(request):
    """Page d'historique des prêts"""
    token = request.session.get('jwt_token')
    if not token:
        messages.error(request, "Session expirée. Reconnectez-vous.")
        return redirect('login')

    # Récupérer l'historique
    loan_service = LoanService(token)
    loans = loan_service.get_loan_history()

    return render(request, 'loan/user_loans.html', {'loans': loans})

@login_required
def loan_approved_view(request):
    """Page de prêt approuvé"""
    return render(request, 'loan/loan_approved.html')

@login_required
def loan_rejected_view(request):
    """Page de prêt rejeté"""
    return render(request, 'loan/loan_rejected.html')
