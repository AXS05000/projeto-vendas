from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import CustomUsuarioCreateForm, LoginForm


@login_required
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        form_login = LoginForm(request.POST)
        form_cadastro = CustomUsuarioCreateForm(request.POST)
        if form_login.is_valid():
            # processa o formulário de login
            pass
        if form_cadastro.is_valid():
            # processa o formulário de cadastro
            pass
    else:
        form_login = LoginForm()
        form_cadastro = CustomUsuarioCreateForm()
    return render(request, 'login.html', {'form_login': form_login, 'form_cadastro': form_cadastro})
