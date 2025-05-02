from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('buttons/', views.button_example, name='button_example'),
    path('js-demo/', views.js_demo, name='js_demo'),
    path('htmx-endpoint/', views.htmx_endpoint, name='htmx_endpoint'),
]

