from django.db import models
from django.db.models import signals
from django.utils import timezone


class Base(models.Model):
    data_de_criacao = models.DateField('Data de Criação', auto_now_add=True)
    data_de_modificacao = models.DateField(
        'Data de Modificação', auto_now=True)

    class Meta:
        abstract = True


class Estoque(Base):
    produto_em_estoque = models.CharField('Produto em Estoque', max_length=54)
    preco_de_venda = models.DecimalField(
        'Preço de Venda', max_digits=18, decimal_places=2, null=True, blank=True)
    preco_de_compra = models.DecimalField(
        'Preço de Compra', max_digits=18, decimal_places=2, null=True, blank=True)
    quantidade_em_estoque = models.DecimalField(
        'Quantidade em Estoque', max_digits=18, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['produto_em_estoque']

    def __str__(self):
        return f'{self.produto_em_estoque}'


class Venda(Base):
    data_da_venda = models.DateTimeField(default=timezone.now)
    quantidade_vendida = models.DecimalField(
        'Quantidade Vendida', max_digits=18, decimal_places=0, null=True, blank=True)
    produto = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True,
    )
    quantidade_vendida2 = models.DecimalField(
        'Quantidade Vendida 2', max_digits=18, decimal_places=0, null=True, blank=True)
    produto2 = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='produto_2',
    )
    quantidade_vendida3 = models.DecimalField(
        'Quantidade Vendida 3', max_digits=18, decimal_places=0, null=True, blank=True)
    produto3 = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='produto_3',
    )
    quantidade_vendida4 = models.DecimalField(
        'Quantidade Vendida 4', max_digits=18, decimal_places=0, null=True, blank=True)
    produto4 = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='produto_4',
    )
    quantidade_vendida5 = models.DecimalField(
        'Quantidade Vendida 5', max_digits=18, decimal_places=0, null=True, blank=True)
    produto5 = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='produto_5',
    )
    quantidade_vendida6 = models.DecimalField(
        'Quantidade Vendida 6', max_digits=18, decimal_places=0, null=True, blank=True)
    produto6 = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='produto_6',
    )
    quantidade_vendida7 = models.DecimalField(
        'Quantidade Vendida 7', max_digits=18, decimal_places=0, null=True, blank=True)
    produto7 = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='produto_7',
    )
    quantidade_vendida8 = models.DecimalField(
        'Quantidade Vendida 8', max_digits=18, decimal_places=0, null=True, blank=True)
    produto8 = models.ForeignKey(
        Estoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='produto_8',
    )

    class Meta:
        ordering = ['data_da_venda']

    def __str__(self):
        return f'{self.data_da_venda} - {self.quantidade_vendida} - {self.produto}'

    @property
    def total_vendido(self):
        return self.produto.preco_de_venda * self.quantidade_vendida

    @property
    def total_lucro(self):
        return (self.produto.preco_de_venda * self.quantidade_vendida) - (self.produto.preco_de_compra * self.quantidade_vendida)
