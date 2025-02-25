# User/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .services import AuthService

def login_view(request):
    """Page de connexion"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Utiliser le service d'authentification
        auth_service = AuthService()
        result = auth_service.login(email, password)

        # Si connexion réussie
        if 'access_token' in result:
            # Stocker le token dans la session
            request.session['jwt_token'] = result['access_token']
            messages.success(request, "Vous êtes connecté!")
            return redirect('user_loans')  # Rediriger vers la page d'historique

        # Si compte non activé
        elif result.get('error') == 'not_activated':
            messages.warning(request, "Votre compte n'est pas activé")
            return redirect('activate_account', email=email)

        # Autres erreurs
        else:
            messages.error(request, "Identifiants invalides")

    return render(request, 'user/login.html')

def activate_account_view(request, email):
    """Page d'activation de compte"""
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier que les mots de passe correspondent
        if new_password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, 'user/activate.html', {'email': email})

        # Activer le compte
        auth_service = AuthService()
        if auth_service.activate_account(email, new_password):
            messages.success(request, "Compte activé avec succès!")
            return redirect('login')
        else:
            messages.error(request, "Échec de l'activation")

    return render(request, 'user/activate.html', {'email': email})

def logout_view(request):
    """Vue de déconnexion"""
    if 'jwt_token' in request.session:
        del request.session['jwt_token']
    messages.success(request, "Vous avez été déconnecté avec succès")
    return redirect('login')