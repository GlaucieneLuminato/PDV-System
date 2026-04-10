# core/models.py (adaptado para Firestore)
from .firebase import db
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

    def salvar(self):
        if self.id:
            db.collection("produtos").document(self.id).update(self.to_dict())
        else:
            doc_ref = db.collection("produtos").document()
            self.id = doc_ref.id
            doc_ref.set(self.to_dict())

    def deletar(self):
        if self.id:
            db.collection("produtos").document(self.id).delete()

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

    @staticmethod
    def listar_todos():
        produtos_ref = db.collection("produtos").stream()
        produtos = []
        for doc in produtos_ref:
            data = doc.to_dict()
            data['id'] = doc.id
            produtos.append(data)
        return produtos


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

    def salvar(self):
        if not self.id:
            doc_ref = db.collection("vendas").document()
            self.id = doc_ref.id
        else:
            doc_ref = db.collection("vendas").document(self.id)

        # Salvar a venda
        doc_ref.set({
            "data_venda": self.data_venda,
            "total": self.total()
        })

        # Salvar itens
        for item in self.itens:
            item.venda_id = self.id
            item.salvar()


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

    def salvar(self):
        if self.quantidade > self.produto.estoque:
            raise ValueError("Estoque insuficiente para este item.")

        if not self.id:
            doc_ref = db.collection("itens_venda").document()
            self.id = doc_ref.id
        else:
            doc_ref = db.collection("itens_venda").document(self.id)

        doc_ref.set({
            "venda_id": self.venda_id,
            "produto_id": self.produto.id,
            "produto_nome": self.produto.nome,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "subtotal": self.subtotal()
        })

        # Atualiza estoque do produto
        self.produto.estoque -= self.quantidade
        self.produto.salvar()

    def deletar(self):
        if self.id:
            db.collection("itens_venda").document(self.id).delete()
            self.produto.estoque += self.quantidade
            self.produto.salvar()


# ------------------------ FUNCIONÁRIO ------------------------
class Funcionario:
    def __init__(self, username, telefone, data_nascimento, cpf, id=None):
        self.id = id
        self.username = username
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def salvar(self):
        if not self.id:
            doc_ref = db.collection("funcionarios").document()
            self.id = doc_ref.id
        else:
            doc_ref = db.collection("funcionarios").document(self.id)

        doc_ref.set({
            "username": self.username,
            "telefone": self.telefone,
            "data_nascimento": self.data_nascimento,
            "cpf": self.cpf
        })

    def deletar(self):
        if self.id:
            db.collection("funcionarios").document(self.id).delete()