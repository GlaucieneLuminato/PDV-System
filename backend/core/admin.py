from django.contrib import admin
from .models import Produto,Venda,ItemVenda

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1

class VendaAdmin(admin.ModelAdmin):
    inlines = [ItemVendaInline]
    list_display = ("id","data_venda","total")

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome","preco","estoque","criado_em")

class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ("venda","produto","quantidade","preco_unitario")



admin.site.register(Produto,ProdutoAdmin)
admin.site.register(Venda,VendaAdmin)
admin.site.register(ItemVenda,ItemVendaAdmin)


