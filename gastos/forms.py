from django import forms
from .models import Gasto, Salario


class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = '__all__'


class SalarioForm(forms.ModelForm):
    class Meta:
        model = Salario
        fields = ['valor']