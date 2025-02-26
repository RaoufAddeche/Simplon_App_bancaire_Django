# user/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib import messages

class JWTAuthMiddleware(MiddlewareMixin):
    """Middleware qui vérifie la présence et la validité du token JWT"""

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Exclure certaines URLs comme login et activation
        excluded_paths = ['/login/', '/activate/', '/admin/']
        if any(request.path.startswith(path) for path in excluded_paths):
            return None

        # Vérifier si l'utilisateur a un token
        if 'jwt_token' not in request.session:
            messages.error(request, "Veuillez vous connecter pour accéder à cette page")
            return redirect('login')

        return None