# core/models.py (corrigido)

from decimal import Decimal
from datetime import datetime


# ------------------------ PRODUTO ------------------------
class Produto:
    def __init__(self, nome, sku, categoria="Eletrônicos", preco_custo=0, preco=0, estoque=0, status=True, id=None):
        self.id = id
        self.nome = nome
        self.sku = sku
        self.categoria = categoria
        self.preco_custo = float(preco_custo)
        self.preco = float(preco)
        self.estoque = int(estoque)
        self.status = status

    def to_dict(self):
        return {
            "nome": self.nome,
            "sku": self.sku,
            "categoria": self.categoria,
            "preco_custo": self.preco_custo,
            "preco": self.preco,
            "estoque": self.estoque,
            "status": self.status
        }


# ------------------------ VENDA ------------------------
class Venda:
    def __init__(self, id=None, data_venda=None):
        self.id = id
        self.data_venda = data_venda or datetime.now()
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def total(self):
        total = Decimal("0.00")
        for item in self.itens:
            total += Decimal(item.subtotal())
        return float(total)


# ------------------------ ITEM VENDA ------------------------
class ItemVenda:
    def __init__(self, produto: Produto, quantidade, preco_unitario=None, venda_id=None, id=None):
        self.id = id
        self.venda_id = venda_id
        self.produto = produto
        self.quantidade = int(quantidade)
        self.preco_unitario = float(preco_unitario or produto.preco)

    def subtotal(self):
        return self.quantidade * self.preco_unitario


# ------------------------ FUNCIONÁRIO ------------------------
class Funcionario:
    def __init__(self, username, telefone, data_nascimento, cpf, id=None):
        self.id = id
        self.username = username
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.cpf = cpf