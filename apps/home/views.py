from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'cotton/home/pages/index.html', {'title': 'Home'})
    # return render(request, 'home/index.html', {'title': 'Home'})


