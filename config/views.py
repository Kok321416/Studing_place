from django.shortcuts import render

def index(request):
    """Главная страница приложения"""
    return render(request, 'index.html')
