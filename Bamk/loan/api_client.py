import requests

API_URL = "http://127.0.0.1:8000"
LOGIN_ENDPOINT = "/auth/login"

def get_auth_token(email, password):
    url = f"{API_URL}{LOGIN_ENDPOINT}"
    payload = {"email": email, "password": password}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Vérifie s'il y a une erreur HTTP
        
        data = response.json()
        return data.get("access_token")  # Adapte selon la structure de réponse de ton API

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'authentification : {e}")
        return None
