from django.urls import path
from .views import loan_request_view, client_history, client_loans, loan_detail, advisor_loans

app_name = "loan"

urlpatterns = [
    #path('connect/', connect_to_api, name='connect_to_api'),
    path("request/", loan_request_view, name="loan_request"),
    path("history", client_history, name="client_history"),
    path("client/loans/", client_loans, name="client_loans"),
    path("client/loans/", client_loans, name="client_loans"),
    path("detail/<int:loan_id>/", loan_detail, name="loan_detail"),
    path("advisor/loans/", advisor_loans, name="advisor_loans"),
    #path("loan/result", loan_request_view, name="loan_request"),
]
