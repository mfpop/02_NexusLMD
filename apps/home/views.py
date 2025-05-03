from django.shortcuts import render


def index(request):
    """View for the home page."""
    return render(request, 'cotton/home/pages/index.html', {'title': 'Home'})


