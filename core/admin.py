#from django.contrib import admin
#from django.urls import path
#from django.shortcuts import render
#from core.firebase import db  # importa sua conexão Firebase

#class FirebaseAdminSite(admin.AdminSite):
#    site_header = "Admin PDV Firebase"

#admin_site = FirebaseAdminSite(name="firebase_admin")

# --- VIEWS CUSTOMIZADAS ---

#def produtos_firebase_view(request):
    # Busca produtos no Firebase
 #   produtos = db.collection("produtos").stream()
  #  context = {"produtos": [p.to_dict() for p in produtos]}
   # return render(request, "admin/produtos.html", context)

#def vendas_firebase_view(request):
 #   vendas = db.collection("vendas").stream()
  #  context = {"vendas": [v.to_dict() for v in vendas]}
   # return render(request, "admin/vendas.html", context)

#def itensvenda_firebase_view(request):
 #   itens = db.collection("itensvenda").stream()
  #  context = {"itens": [i.to_dict() for i in itens]}
   # return render(request, "admin/itensvenda.html", context)

# --- REGISTRO DAS URLs CUSTOMIZADAS ---

#def get_urls():
 #   urls = [
  #      path('produtos/', admin_site.admin_view(produtos_firebase_view), name='produtos'),
   #     path('vendas/', admin_site.admin_view(vendas_firebase_view), name='vendas'),
    #    path('itensvenda/', admin_site.admin_view(itensvenda_firebase_view), name='itensvenda'),
    #]
 #   return urls + admin_site.get_urls_original()

# Mantém a URL padrão do Django Admin
#admin_site.get_urls_original = admin_site.get_urls
#admin_site.get_urls = get_urls