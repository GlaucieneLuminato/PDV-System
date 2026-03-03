from django.db import models
from django.core.exceptions import ValidationError

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.nome

class Venda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    data_venda = models.DateTimeField(auto_now_add=True)

    
    def clean(self):
        if self.quantidade > self.produto.estoque:
            raise ValidationError("Estoque insuficiente para realizar a venda.")
    def save(self, *args,**kwargs):
        self.full_clean()
        self.total = self.produto.preco * self.quantidade
        self.produto.estoque -= self.quantidade
        self.produto.save()
        super().save(*args,**kwargs)

    def __str__(self):
        return f"Vendas #{self.id}"


# Create your models here.
