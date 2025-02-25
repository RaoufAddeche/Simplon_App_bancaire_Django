from django.urls import path
from .views import create_news, list_news

urlpatterns = [
    path('', list_news, name='list_articles'),
    path("news/create/", create_news, name="create_news")
]
