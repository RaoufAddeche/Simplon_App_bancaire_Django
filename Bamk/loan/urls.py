from django.urls import path
from .views import loan_request_view, client_history, client_loans

app_name = "loan"

urlpatterns = [
    #path('connect/', connect_to_api, name='connect_to_api'),
    path("request/", loan_request_view, name="loan_request"),
    path("history", client_history, name="client_history"),
    path("client/loans/", client_loans, name="client_loans"),
    #path("loan/result", loan_request_view, name="loan_request"),
]
