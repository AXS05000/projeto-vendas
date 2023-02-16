from django import forms

from .models import Venda


class VendaModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Venda
        fields = ('quantidade_vendida', 'produto', 'quantidade_vendida2',
                  'produto2', 'quantidade_vendida3', 'produto3', 'quantidade_vendida4',
                  'produto4', 'quantidade_vendida5', 'produto5', 'quantidade_vendida6',
                  'produto6', 'quantidade_vendida7', 'produto7', 'quantidade_vendida8',
                  'produto8')
        required = ['quantidade_vendida', 'produto']
