from datetime import datetime

from django import forms
from django.contrib import messages
from django.db.models import F, FloatField, Q, Sum
from django.db.models.functions import (ExtractMonth, ExtractWeekDay,
                                        ExtractYear)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
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


class VendaListView(ListView):
    model = Venda
    template_name = 'sale_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        v = Venda.objects.all()

        context['v'] = v

        total_vendas = v.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).aggregate(total=Sum('total_value'))['total'] or 0

        context['total_vendas'] = total_vendas

        total_de_lucros = v.annotate(
            total_lucro=Sum(
                (F('produto__preco_de_venda') * F('quantidade_vendida')) -
                (F('produto__preco_de_compra') * F('quantidade_vendida')),
                output_field=FloatField()
            )
        ).aggregate(total=Sum('total_lucro'))['total'] or 0

        context['total_de_lucros'] = total_de_lucros

        return context


class DashListView(ListView):
    model = Venda
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total de vendas
        v2 = Venda.objects.all()
        context['v2'] = v2
        total_vendas2 = v2.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).aggregate(total=Sum('total_value'))['total'] or 0
        context['total_vendas2'] = total_vendas2

        # Total de lucros
        total_de_lucros2 = v2.annotate(
            total_lucro=Sum(
                (F('produto__preco_de_venda') * F('quantidade_vendida')) -
                (F('produto__preco_de_compra') * F('quantidade_vendida')),
                output_field=FloatField()
            )
        ).aggregate(total=Sum('total_lucro'))['total'] or 0
        context['total_de_lucros2'] = total_de_lucros2

        # Total de vendas na semana atual
        semana_atual = timezone.now().isocalendar()[
            1]  # número da semana atual
        total_vendas_semana_atual = v2.filter(data_da_venda__week=semana_atual).aggregate(
            total=Sum(F('produto__preco_de_venda') * F('quantidade_vendida'), output_field=FloatField()))['total'] or 0
        context['total_vendas_semana_atual'] = total_vendas_semana_atual

        total_lucro_semana_atual = v2.filter(data_da_venda__week=semana_atual).aggregate(
            total=Sum((F('produto__preco_de_venda') * F('quantidade_vendida')) -
                      (F('produto__preco_de_compra') * F('quantidade_vendida')), output_field=FloatField()))['total'] or 0
        context['total_lucro_semana_atual'] = total_lucro_semana_atual

        mes_atual = timezone.now().month
        total_vendas_mes_atual = v2.filter(data_da_venda__month=mes_atual).aggregate(
            total=Sum(F('produto__preco_de_venda') * F('quantidade_vendida'), output_field=FloatField()))['total'] or 0
        context['total_vendas_mes_atual'] = total_vendas_mes_atual

        total_lucro_mes_atual = v2.filter(data_da_venda__month=mes_atual).aggregate(
            total=Sum((F('produto__preco_de_venda') * F('quantidade_vendida')) -
                      (F('produto__preco_de_compra') * F('quantidade_vendida')), output_field=FloatField()))['total'] or 0
        context['total_lucro_mes_atual'] = total_lucro_mes_atual

        # Porcentagem de vendas comparada com o mês anterior
        last_month_sales = Venda.objects.filter(data_da_venda__month=timezone.now().month-1).aggregate(
            total=Sum(F('produto__preco_de_venda') * F('quantidade_vendida'), output_field=FloatField()))['total'] or 0
        current_month_sales = total_vendas_mes_atual
        if last_month_sales == 0:
            percentual_vendas = '-'
        else:
            percentual_vendas = round(
                (current_month_sales-last_month_sales)/last_month_sales*100, 2)
        context['percentual_vendas'] = percentual_vendas

        # Porcentagem de vendas comparada com o mês anterior
        last_month_sales2 = Venda.objects.filter(data_da_venda__month=timezone.now().month-1).aggregate(
            total=Sum((F('produto__preco_de_venda') * F('quantidade_vendida')) -
                      (F('produto__preco_de_compra') * F('quantidade_vendida')), output_field=FloatField()))['total'] or 0
        current_month_sales2 = total_lucro_mes_atual
        if last_month_sales2 == 0:
            percentual_vendas2 = '-'
        else:
            percentual_vendas2 = round(
                (current_month_sales2-last_month_sales2)/last_month_sales2*100, 2)
        context['percentual_vendas2'] = percentual_vendas2

        # Porcentagem de vendas comparada com a semana anterior
        last_week_sales = Venda.objects.filter(data_da_venda__week=timezone.now().isocalendar()[1]-1).aggregate(
            total=Sum(F('produto__preco_de_venda') * F('quantidade_vendida'), output_field=FloatField()))['total'] or 0
        current_week_sales = total_vendas_semana_atual
        if last_week_sales == 0:
            percentual_vendas_semana_anterior = '-'
        else:
            percentual_vendas_semana_anterior = round(
                (current_week_sales-last_week_sales)/last_week_sales*100, 2)
        context['percentual_vendas_semana_anterior'] = percentual_vendas_semana_anterior

        # Porcentagem de vendas comparada com a semana anterior 2
        last_week_sales2 = Venda.objects.filter(data_da_venda__week=timezone.now().isocalendar()[1]-1).aggregate(
            total=Sum((F('produto__preco_de_venda') * F('quantidade_vendida')) -
                      (F('produto__preco_de_compra') * F('quantidade_vendida')), output_field=FloatField()))['total'] or 0
        current_week_sales2 = total_lucro_semana_atual
        if last_week_sales2 == 0:
            percentual_vendas_semana_anterior2 = '-'
        else:
            percentual_vendas_semana_anterior2 = round(
                (current_week_sales2-last_week_sales2)/last_week_sales2*100, 2)
        context['percentual_vendas_semana_anterior2'] = percentual_vendas_semana_anterior2

        # Total de Vendas Segunda Feira

        segunda_feira_vendas = Venda.objects.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).filter(data_da_venda__week=timezone.now().isocalendar()[1], data_da_venda__week_day=2).aggregate(total=Sum('total_value'))['total'] or 0
        context['segunda_feira_vendas'] = segunda_feira_vendas

        # Total de Vendas Terça Feira

        terca_feira_vendas = Venda.objects.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).filter(data_da_venda__week=timezone.now().isocalendar()[1], data_da_venda__week_day=3).aggregate(total=Sum('total_value'))['total'] or 0
        context['terca_feira_vendas'] = terca_feira_vendas

        # Total de Vendas Quarta Feira

        quarta_feira_vendas = Venda.objects.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).filter(data_da_venda__week=timezone.now().isocalendar()[1], data_da_venda__week_day=4).aggregate(total=Sum('total_value'))['total'] or 0
        context['quarta_feira_vendas'] = quarta_feira_vendas

        # Total de Vendas Quinta Feira

        quinta_feira_vendas = Venda.objects.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).filter(data_da_venda__week=timezone.now().isocalendar()[1], data_da_venda__week_day=5).aggregate(total=Sum('total_value'))['total'] or 0
        context['quinta_feira_vendas'] = quinta_feira_vendas

        # Total de Vendas Sexta Feira
        sexta_feira_vendas = Venda.objects.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).filter(data_da_venda__week=timezone.now().isocalendar()[1], data_da_venda__week_day=6).aggregate(total=Sum('total_value'))['total'] or 0
        context['sexta_feira_vendas'] = sexta_feira_vendas

        # Total de Vendas Sabado
        sabado_vendas = Venda.objects.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).filter(data_da_venda__week=timezone.now().isocalendar()[1], data_da_venda__week_day=7).aggregate(total=Sum('total_value'))['total'] or 0
        context['sabado_vendas'] = sabado_vendas

        # Total de Vendas Domingo
        domingo_vendas = Venda.objects.annotate(
            total_value=Sum(
                F('produto__preco_de_venda') * F('quantidade_vendida'),
                output_field=FloatField()
            )
        ).filter(data_da_venda__week=timezone.now().isocalendar()[1], data_da_venda__week_day=1).aggregate(total=Sum('total_value'))['total'] or 0
        context['domingo_vendas'] = domingo_vendas

        context['sales_data'] = [
            segunda_feira_vendas,
            terca_feira_vendas,
            quarta_feira_vendas,
            quinta_feira_vendas,
            sexta_feira_vendas,
            sabado_vendas,
            domingo_vendas,
        ]

        mes = 1
        ano = datetime.now().year

        total_vendas_janeiro = Venda.objects.filter(data_da_venda__month=mes, data_da_venda__year=ano).aggregate(
            total=Sum(F('produto__preco_de_venda') * F('quantidade_vendida'), output_field=FloatField()))['total'] or 0
        context['total_vendas_janeiro'] = total_vendas_janeiro

        return context


def tables(request):
    return render(request, 'pages/tables.html')


def billing(request):
    return render(request, 'pages/billing.html')


def virtual_reality(request):
    return render(request, 'pages/virtual-reality.html')


def rtl(request):
    return render(request, 'pages/rtl.html')


def notifications(request):
    return render(request, 'pages/notifications.html')


def profile(request):
    return render(request, 'pages/profile.html')


def sign_in(request):
    return render(request, 'pages/sign-in.html')


def sign_up(request):
    return render(request, 'pages/sign-up.html')
