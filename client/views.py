from django.shortcuts import render, redirect
from .forms import ClientInformationForm

def home(request):
    return render(request, 'client/home.html')

def register_client(request):
    if request.method == 'POST':
        form = ClientInformationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientInformationForm()
    return render(request, 'client/register_client.html', {'form': form})