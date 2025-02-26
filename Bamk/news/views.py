from django.shortcuts import render, redirect
from .models import News
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewsForm

def list_news(request):
    articles = News.objects.all()
    print("Articles récupérés :", articles)
    context = {
        'news' : articles
    }
    return render(request, "news/list_articles.html", {"news": articles})

@login_required
def create_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, user=request.user)  # ✅ Passe user correctement
        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user  # ✅ Assigne l'auteur automatiquement
            news.save()
            messages.success(request, "Votre article a été publié avec succès.")
            return redirect("news_list")  # ✅ Redirige après la création
    else:
        form = NewsForm(user=request.user)  # ✅ Passe user aussi pour GET

    return render(request, "news/write_article.html", {"form": form})
