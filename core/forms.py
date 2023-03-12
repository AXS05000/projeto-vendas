from django import forms

from .models import Venda


class VendaModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Venda
        fields = ('quantidade_vendida', 'produto')
        required = ['quantidade_vendida', 'produto']
