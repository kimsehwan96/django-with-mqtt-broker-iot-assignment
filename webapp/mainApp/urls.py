from django.urls import path, include

from . import views

app_name = 'mainApp'
urlpatterns = [
    path('', views.TemplateView.as_view(), name='index'),
]