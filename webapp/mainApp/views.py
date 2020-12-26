import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.views import generic

class TemplateView(generic.TemplateView):
    template_name = 'mainApp/index.html'
    print("hello!")