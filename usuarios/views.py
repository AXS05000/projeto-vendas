from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import CustomUsuarioCreateForm, LoginForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email ou senha incorretos')
    return render(request, 'registration/login.html', {'error': messages.get_messages(request)})


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')
