from django.shortcuts import render


def index(request):
  return render(request, 'production/pages/index.html', {'title': 'Production'})