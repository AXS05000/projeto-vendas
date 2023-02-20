from django.contrib import admin

from .models import Estoque, Venda

# Register your models here.


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto_em_estoque', 'preco_de_venda', 'preco_de_compra',
                    'quantidade_em_estoque')


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('data_da_venda', 'quantidade_vendida', 'produto', 'quantidade_vendida2',
                    'produto2', 'quantidade_vendida3', 'produto3', 'quantidade_vendida4',
                    'produto4', 'quantidade_vendida5', 'produto5', 'quantidade_vendida6',
                    'produto6', 'quantidade_vendida7', 'produto7', 'quantidade_vendida8',
                    'produto8')
