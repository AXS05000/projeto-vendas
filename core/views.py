import datetime

from django import forms
from django.contrib import messages
from django.db.models import F, FloatField, Q, Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import VendaModelForm
from .models import Estoque, Venda


def index(request):
    return render(request, 'index.html')


class FormularioDeVendaCreateView(CreateView):
    model = Venda
    form_class = VendaModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estoque'] = Estoque.objects.all()
        return context

    success_url = reverse_lazy('formulariodevenda')
    template_name = 'formulariodevenda.html'

    def form_valid(self, form):
        # Verifica a quantidade em estoque do produto selecionado
        produto = form.cleaned_data['produto']
        quantidade_vendida = form.cleaned_data['quantidade_vendida']
        if produto.quantidade_em_estoque < quantidade_vendida:
            form.add_error(
                'quantidade_vendida', 'Quantidade em estoque insuficiente.')
            return self.form_invalid(form)

        # Salva a venda e atualiza a quantidade em estoque
        venda = form.save(commit=False)
        venda.save()
        produto.quantidade_em_estoque -= quantidade_vendida
        produto.save()

        return super().form_valid(form)


def login(request):
    return render(request, 'login.html')
