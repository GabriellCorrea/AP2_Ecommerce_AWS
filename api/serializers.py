from rest_framework import serializers
from .models import Produto, Loja, Pedido, ItemPedido

IMAGEM_TIPOS_PERMITIDOS = ['image/jpeg', 'image/png', 'image/webp']
IMAGEM_TAMANHO_MAXIMO_MB = 5


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        read_only_fields = ('criado_em', 'atualizado_em')

    def validate_imagem(self, arquivo):
        if arquivo is None:
            return arquivo

        if arquivo.content_type not in IMAGEM_TIPOS_PERMITIDOS:
            raise serializers.ValidationError(
                f"Tipo de arquivo não permitido: {arquivo.content_type}. "
                f"Use JPEG, PNG ou WebP."
            )

        limite_bytes = IMAGEM_TAMANHO_MAXIMO_MB * 1024 * 1024
        if arquivo.size > limite_bytes:
            raise serializers.ValidationError(
                f"Arquivo muito grande ({arquivo.size / 1024 / 1024:.1f} MB). "
                f"O limite é {IMAGEM_TAMANHO_MAXIMO_MB} MB."
            )

        return arquivo


class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ('criado_em',)


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = '__all__'
