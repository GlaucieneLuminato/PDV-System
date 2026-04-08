from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet, UserViewSet
from .views import me, criar_funcionario, teste_debug, dashboard
from rest_framework_simplejwt.views import TokenObtainPairView

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
    path("teste/", teste_debug),

    path("", include(router.urls)),
]