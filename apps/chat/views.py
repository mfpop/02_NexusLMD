from django.shortcuts import render


# Create your views here.
def index(request):
  return render(request, 'chat/pages/index.html', {'title': 'Chat'})
