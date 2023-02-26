from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import CustomUsuarioCreateForm, LoginForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_field_name = 'ne'


def login_view(request):
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
    return CustomLoginView.as_view()(request, **{'form': form_login})


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')
