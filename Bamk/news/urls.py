from django.urls import path
from .views import create_news, list_news

app_name = 'news'

urlpatterns = [
    path('', list_news, name='news_list'),
    path("create/", create_news, name="create_news")
]
