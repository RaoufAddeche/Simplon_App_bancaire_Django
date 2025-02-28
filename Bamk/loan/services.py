# loan/services.py
import requests
from django.conf import settings

class LoanAPIService:
    """Service pour communiquer avec l'API FastAPI pour les prêts"""

    @staticmethod
    def get_jwt_token(request):
        """Récupère le token JWT de la session utilisateur"""
        return request.session.get('jwt_token')

    @staticmethod
    def get_loan_history(request):
        """Récupère l'historique des prêts de l'utilisateur"""
        token = LoanAPIService.get_jwt_token(request)
        if not token:
            return {"error": "authentication_error"}

        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{settings.FASTAPI_BASE_URL}/loans/history",
                headers=headers
            )

            if response.status_code == 200:
                return response.json()
            return {"error": "api_error", "status": response.status_code}
        except Exception as e:
            return {"error": "connection_error", "message": str(e)}

    @staticmethod
    def submit_loan_request(request, loan_data):
        """Soumet une demande de prêt à l'API"""
        token = LoanAPIService.get_jwt_token(request)
        if not token:
            return {"error": "authentication_error"}

        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/loans/request",
                headers=headers,
                json=loan_data
            )

            if response.status_code == 200:
                return response.json()
            return {"error": "api_error", "status": response.status_code}
        except Exception as e:
            return {"error": "connection_error", "message": str(e)}

    @staticmethod
    def get_advisor_loans(request):
        """Récupère les prêts des clients pour un conseiller"""
        token = LoanAPIService.get_jwt_token(request)
        if not token:
            return {"error": "authentication_error"}

        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{settings.FASTAPI_BASE_URL}/loans/advisor",
                headers=headers
            )

            if response.status_code == 200:
                return response.json()
            return {"error": "api_error", "status": response.status_code}
        except Exception as e:
            return {"error": "connection_error", "message": str(e)}
