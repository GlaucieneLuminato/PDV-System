from django .urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProdutoViewSet, VendaViewSet, ItemVendaViewSet
from django.urls import path
from .views_api import dashboard
from rest_framework_simplejwt.views import TokenObtainPairView
from .views_api import UserViewSet
from .views import me

router = DefaultRouter()
router.register(r'produtos',ProdutoViewSet)
router.register(r'vendas',VendaViewSet)
router.register(r'itens',ItemVendaViewSet)
router.register(r'users',UserViewSet)

urlpatterns = [
    
    path("dashboard/", dashboard, name="dashboard"), 
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('me/',me),
   
    path("", include(router.urls)),
]

