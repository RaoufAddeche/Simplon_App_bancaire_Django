# Loan/services.py
import requests
from django.conf import settings

class LoanService:
    """Service pour communiquer avec l'API de prêts"""

    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_loan_history(self):
        """Récupère l'historique des prêts de l'utilisateur"""
        try:
            response = requests.get(
                f"{settings.FASTAPI_BASE_URL}/loans/history",
                headers=self.headers
            )

            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []

    def submit_loan_request(self, loan_data):
        """Envoie une demande de prêt à l'API"""
        try:
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/loans/request",
                headers=self.headers,
                json=loan_data
            )

            if response.status_code == 200:
                return response.json()
            return {"error": "submission_failed"}
        except Exception as e:
            return {"error": "api_error", "message": str(e)}