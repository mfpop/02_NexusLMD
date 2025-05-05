from django.shortcuts import render


def index(request):
    """View for the Contact page."""
    return render(request, 'cotton/contact/pages/index.html', {'title': 'Contact Us'})