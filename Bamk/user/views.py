from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from .forms import UserCreationForm
from .models import User


class HomeView(TemplateView):
    template_name = 'home.html'

class RegisterView(CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('client')

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        """Handles POST requests for login, authenticates user."""
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            redirect_url = 'advisor' if user.is_staff else 'client'
            return redirect(redirect_url)
        
        messages.error(request, "Incorrect username or password")
        return redirect('client')

class ClientView(LoginRequiredMixin, TemplateView):
    template_name = 'client.html'

class AdvisorView(LoginRequiredMixin, TemplateView):
    template_name = 'advisor.html'