from django.urls import path
from .views import  loan_request_view

urlpatterns = [
    #path('connect/', connect_to_api, name='connect_to_api'),
    path("request/", loan_request_view, name="loan_request"),
    #path("loan/result", loan_request_view, name="loan_request"),
]
