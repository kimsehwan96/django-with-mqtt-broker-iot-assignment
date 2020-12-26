from django.urls import path

from . import views

app_name = 'mainApp'
urlpatterns = [
    path('', views.TemplateView.as_view(), name='index')
]