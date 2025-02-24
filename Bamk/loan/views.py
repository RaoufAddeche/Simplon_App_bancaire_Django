from django.shortcuts import render ,redirect
from .models import Loan
from .forms import LoanRequestForm
from user.services import FastAPIClient #classe pour interagir avec fastapi
from django.contrib.auth.decorators import login_required

FASTAPI_BASE_URL = "http://127.0.0.1:8000/api"  # URL de base de l'API FastAPI

@login_required
def loan_request(request):
    "Vue pour soumettre une demande de prêt"
    if request.method == "POST":
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            token = request.session.get("access_token")
            if not token :
                return render(request, "error.html", {"message": "Utilisateur non authentifié."})
            
            #Récuperer le montant du formulaire
            amount = form.cleaned_data["amount"]

            #Appeler fastapi pour créer une demande de prêt
            client= FastAPIClient(base_url = FASTAPI_BASE_URL)
            loan_data= client.create_loan_request(token, amount)

            if not loan_data:
                return render(request, "error.html", {"message": "Impossible de soumettre la demande de prêt."})
            
            #Enregistrer la demande localement
            Loan.objects.create(
                user=request.user,
                amount=amount,
                status=loan_data.get("status","pending")
            )

            #Si le prêt est refusé, affiche une notif immédiatement
            if loan_data.get("status") == "rejected":
                return render(request, "loan/loan_rejected.html", {"loan": loan_data})
            
            #si le prêt est accepté, rediriger vers un conseiller
            if loan_data.get("status") == "approved":
                return render(request, "loan/loan_approved.html", {"loan":loan_data})
            
    else:
        form = LoanRequestForm()
    return render(request, "loan/loan_request.html", {"form": form})




@login_required
def user_loans(request):
    """
    Vue pour afficher l'historique des prêts d'un utilisateur.
    """
    loans = Loan.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "loan/user_loan.html", {"loans": loans})

@login_required
def advisor_loans(request):
    """
    Vue pour afficher les prêts assignés à un conseiller.
    """
    if not request.user.is_staff:  # Vérifier si l'utilisateur est un conseiller
        return render(request, "error.html", {"message": "Accès non autorisé."})

    loans = Loan.objects.filter(assigned_to=request.user).order_by("-created_at")
    return render(request, "loan/advisor_loan.html", {"loans": loans})