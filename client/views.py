from django.shortcuts import render, redirect

def home(request):
    return render(request, 'client/home.html')

def register(request):
    return render(request, 'client/register.html')