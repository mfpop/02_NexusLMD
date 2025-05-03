from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    """View for the Contact page."""
    return render(request, 'cotton/contact/pages/index.html', {'title': 'Contact Us'})