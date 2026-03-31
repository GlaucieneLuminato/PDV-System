from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet, dashboard, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import me
from .views import me, criar_funcionario

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'itens', ItemVendaViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"), 
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("me/", me),
    path("criar-funcionario/", criar_funcionario),

    path("", include(router.urls)),
]