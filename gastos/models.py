from django.db import models


class Gasto(models.Model):
    CATEGORIAS = [
        ('Alimentação', 'Alimentação'),
        ('Transporte', 'Transporte'),
        ('Moradia', 'Moradia'),
        ('Saúde', 'Saúde'),
        ('Lazer', 'Lazer'),
        ('Educação', 'Educação'),
        ('Outros', 'Outros'),
    ]

    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    data = models.DateField()

    def __str__(self):
        return self.descricao


class Salario(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"R$ {self.valor}"
