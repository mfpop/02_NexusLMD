from django.shortcuts import render


def index(request):
    """View for the About page."""
    return render(request, 'cotton/about/pages/index.html', {'title': 'About'})