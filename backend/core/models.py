from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    sku = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100, default = "Eletrônicos")
    preco_custo = models.DecimalField(max_digits=10, decimal_places = 2, default = 0)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    status = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.nome

class Venda(models.Model):
  data_venda = models.DateTimeField(auto_now_add=True)

  def __str__(self):
     return f"Venda #{self.id}"

  def total(self):
    total = Decimal("0.00")
    for item in self.itens.all():
        total += item.subtotal()
    return total
  total.short_description = "Total"
    
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name= "itens", on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete= models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    def clean(self):
     if self.quantidade > self.produto.estoque:
        raise ValidationError("Estoque insuficiente para este item.")

    
    def subtotal(self):
                    return self.quantidade * self.preco_unitario
            
    def save(self,*args,**kwargs):
                self.full_clean()

                if not self.preco_unitario:
                    self.preco_unitario = self.produto.preco
                if not self.pk:
                    if self.quantidade > self.produto.estoque:
                        raise ValidationError("Estoque insuficiente.")
                    self.produto.estoque -= self.quantidade
                    self.produto.save()

                    super().save(*args, **kwargs)

    def delete(self,*args,**kwargs):
                    self.produto.estoque += self.quantidade
                    self.produto.save()
                    super().delete(*args,**kwargs)
                    
    def __str__(self):
                    return f"{self.produto.nome} - {self.quantidade}"
                

        
class Funcionario(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)
    
    is_admin = models.BooleanField(default=False)
    def __str__(self):return self.user.username

class Usuario(AbstractBaseUser):
    TIPO_USUARIO = (
        ('admin', 'Administrador'),
        ('funcionario','Funcionario'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
# Create your models here.
