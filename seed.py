import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lanchonete.settings')
django.setup()

from cardapio.models import Categoria, Produto

dados = {
    'Lanches': [('X-Burger', '18.50'), ('X-Salada', '20.00'), ('X-Bacon', '24.00'), ('Hot Dog', '12.00')],
    'Bebidas': [('Refrigerante Lata', '6.00'), ('Suco de Laranja', '8.00'), ('Água', '4.00')],
    'Sobremesas': [('Pudim', '9.00'), ('Sorvete', '7.50'), ('Brownie', '10.00')],
}

for nome_cat, produtos in dados.items():
    categoria, _ = Categoria.objects.get_or_create(nome=nome_cat)
    for nome, preco in produtos:
        Produto.objects.get_or_create(nome=nome, categoria=categoria, defaults={'preco': preco})

print('Pronto:', Categoria.objects.count(), 'categorias e', Produto.objects.count(), 'produtos')