from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to Login..')
            return redirect('login')
    else:        
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form':form})
