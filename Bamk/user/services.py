import requests



class FastAPIClient:
    """classe pour interagir avec FastAPI"""
    def __init__(self,base_url):
        self.base_url = base_url
    
    def create_loan_request(self, token, amount):
        """Crée une demande de prêt via FASTAPI"""
        url = f"{self.base_url}/loans/request"
        headers = {"Authorization": f"Bearer{token}"}
        data = {"amount": amount}
        
        try:
            response = requests.post(url, headers = headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"erreur lors de l'appel à FASTAPI: {e}")
            return None