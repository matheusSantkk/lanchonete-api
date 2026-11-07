import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Categoria, Produto
from .serializers import CategoriaSerializer, ProdutoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer

    @action(detail=True, methods=['get'])
    def produtos(self, request, pk=None):
        categoria = self.get_object()
        serializer = ProdutoSerializer(categoria.produtos.all(), many=True)
        return Response(serializer.data)


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria').order_by('id')
    serializer_class = ProdutoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nome']

    def get_queryset(self):
        queryset = super().get_queryset()
        disponivel = self.request.query_params.get('disponivel')
        if disponivel is not None:
            queryset = queryset.filter(disponivel=disponivel.lower() == 'true')
        return queryset


class MunicipiosView(APIView):
    def get(self, request):
        uf = request.query_params.get('uf', '').strip().upper()
        if len(uf) != 2 or not uf.isalpha():
            return Response({'erro': 'Informe uma UF válida, ex.: ?uf=PE'},
                            status=status.HTTP_400_BAD_REQUEST)

        url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios'
        try:
            resposta = requests.get(url, timeout=10)
        except (requests.Timeout, requests.ConnectionError):
            return Response({'erro': 'IBGE indisponível no momento. Tente mais tarde.'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        if resposta.status_code >= 500:
            return Response({'erro': 'IBGE indisponível no momento. Tente mais tarde.'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        dados = resposta.json()
        if not isinstance(dados, list) or not dados:
            return Response({'erro': f'UF "{uf}" não encontrada.'},
                            status=status.HTTP_400_BAD_REQUEST)

        municipios = [{'codigo_ibge': m['id'], 'nome': m['nome']} for m in dados]
        return Response({'uf': uf, 'total': len(municipios), 'municipios': municipios})