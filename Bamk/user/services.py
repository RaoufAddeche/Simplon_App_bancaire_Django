# User/services.py
import requests
from django.conf import settings

class AuthService:
    """Service pour communiquer avec l'API d'authentification"""

    def login(self, email, password):
        """Connecte un utilisateur via l'API"""
        try:
            # Envoie une requête POST à l'API
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/auth/login",
                json={"email": email, "password": password}
            )

            # Si la connexion réussit
            if response.status_code == 200:
                return response.json()  # Retourne le token JWT

            # Si le compte n'est pas activé
            elif response.status_code == 403:
                return {"error": "not_activated"}

            # Autres erreurs
            else:
                return {"error": "login_failed"}

        except Exception as e:
            return {"error": "api_error", "message": str(e)}

    def activate_account(self, email, new_password):
        """Active un compte utilisateur"""
        try:
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/auth/activation",
                json={"email": email, "new_password": new_password}
            )
            return response.status_code == 200
        except Exception:
            return False