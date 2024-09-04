from django.shortcuts import render, redirect
from .forms import ClientInformationForm

def home(request):
    return render(request, 'client/home.html')

