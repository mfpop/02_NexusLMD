from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'cotton/home/pages/index.html', {'title': 'Home'})

def button_example(request):
    return render(
        request,
        'cotton/home/components/button_example.html',
        {'title': 'Button Examples'}
    )

def js_demo(request):
    """View to demonstrate Alpine.js and htmx functionality."""
    return render(request, 'cotton/home/pages/js_demo.html', {'title': 'Alpine.js and htmx Demo'})

def htmx_endpoint(request):
    """Simple endpoint for htmx requests demonstration."""
    return HttpResponse("<div class='bg-green-200 p-4 rounded-lg'>HTMX loaded this content dynamically!</div>")