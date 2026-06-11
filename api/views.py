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

    - GET /api/produtos/                        → lista todos
    - GET /api/produtos/?marca=Dell             → filtra por atributo JSON (marca)
    - GET /api/produtos/?cor=preto              → filtra por atributo JSON (cor)
    - GET /api/produtos/?marca=Dell&cor=preto   → filtro combinado relacional + JSON
    - POST /api/produtos/                       → cria novo
    - GET /api/produtos/{id}/                   → detalhe
    - PUT /api/produtos/{id}/                   → atualiza
    - DELETE /api/produtos/{id}/                → remove
    """
    serializer_class = ProdutoSerializer

    # Atributos JSON aceitos como query params para filtro
    ATRIBUTOS_FILTRO = ['marca', 'cor', 'ram_gb', 'tamanho', 'voltagem']

    def get_queryset(self):
        qs = Produto.objects.all()

        # Filtros relacionais convencionais
        loja_id = self.request.query_params.get('loja')
        if loja_id:
            qs = qs.filter(loja_id=loja_id)

        # Filtros dentro do campo JSON atributos
        for atributo in self.ATRIBUTOS_FILTRO:
            valor = self.request.query_params.get(atributo)
            if valor:
                qs = qs.filter(**{f'atributos__{atributo}': valor})

        return qs


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
