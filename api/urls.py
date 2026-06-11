from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'produtos', views.ProdutoViewSet, basename='produto')
router.register(r'loja', views.LojaViewSet, basename='loja')
router.register(r'pedido', views.PedidoViewSet, basename='pedido')
router.register(r'itens-pedido', views.ItemPedidoViewSet, basename='itens-pedido')


urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('', include(router.urls)),
]
