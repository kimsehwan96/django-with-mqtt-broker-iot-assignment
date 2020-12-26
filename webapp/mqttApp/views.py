from typing import ContextManager
from django import template
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.views import generic
from .models import Data


class IndexView(generic.ListView):
    template_name = 'mqttApp/index.html'
    context_object_name = 'latest_data_list'

    def get_queryset(self):
        return Data.objects.order_by('-timestamp')[:10]

class DetailView(generic.DetailView):
    model = Data
    template_name = 'mqttApp/detail.html'