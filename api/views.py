from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Produto, Loja, Pedido, ItemPedido
from .serializers import (
    ProdutoSerializer,
    LojaSerializer,
    PedidoSerializer,
    ItemPedidoSerializer
)


@api_view(['GET'])
def health_check(request):
    """Endpoint de saúde — usado pelo EB para verificar se a app está no ar."""
    return Response({
        'status': 'ok',
        'mensagem': 'API funcionando!'
    })


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Produtos.

    - GET /api/produtos/ → lista todos 
    - POST /api/produtos/ → cria novo 
    - GET /api/produtos/{id}/ → detalhe 
    - PUT /api/produtos/{id}/ → atualiza 
    - DELETE /api/produtos/{id}/ → remove

    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class LojaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Lojas.

    - GET    /api/lojas/        → lista todas
    - POST   /api/lojas/        → cria nova
    - GET    /api/lojas/{id}/   → detalhe
    - PUT    /api/lojas/{id}/   → atualiza
    - DELETE /api/lojas/{id}/   → remove

    """
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Pedidos.

    - GET    /api/pedidos/        → lista todos
    - POST   /api/pedidos/        → cria novo
    - GET    /api/pedidos/{id}/   → detalhe
    - PUT    /api/pedidos/{id}/   → atualiza
    - DELETE /api/pedidos/{id}/   → remove
    
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class ItemPedidoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Itens de Pedido.

    - GET    /api/itens-pedido/        → lista todos
    - POST   /api/itens-pedido/        → cria novo
    - GET    /api/itens-pedido/{id}/   → detalhe
    - PUT    /api/itens-pedido/{id}/   → atualiza
    - DELETE /api/itens-pedido/{id}/   → remove

    """
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer
