from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Cliente, Restaurante, Produto, Pedido, ItemPedido, CategoriaProduto 
from .services.produto_service import ProdutoService 
from .services.pedido_service import PedidoService   

def homepage(request):
    produto_service = ProdutoService()
    produtos_em_destaque = produto_service.get_all_produtos()[:3] 

    context = {
        'produtos_em_destaque': produtos_em_destaque
    }
    return render(request, 'homepage.html', context)

def login_page(request):
    return render(request, 'login_page.html')


def catalogo1(request):
    produto_service = ProdutoService()
    produtos = produto_service.get_produtos_by_categoria(categoria_id=1)
    context = {'produtos': produtos}
    return render(request, 'catalogo1.html', context)

def catalogo2(request):
    produto_service = ProdutoService()
    produtos = produto_service.get_produtos_by_categoria(categoria_id=2)
    context = {'produtos': produtos}
    return render(request, 'catalogo2.html', context)

def catalogo3(request):
    produto_service = ProdutoService()
    produtos = produto_service.get_produtos_by_categoria(categoria_id=3)
    context = {'produtos': produtos}
    return render(request, 'catalogo3.html', context)

def catalogo4(request):
    produto_service = ProdutoService()
    produtos = produto_service.get_produtos_by_categoria(categoria_id=4)
    context = {'produtos': produtos}
    return render(request, 'catalogo4.html', context)
def criar_pedido(request):
    pedido_service = PedidoService()
    produto_service = ProdutoService() 

    if request.method == 'POST':

        try:
            cliente = Cliente.objects.first()
            restaurante = Restaurante.objects.first()

            if not cliente:
                return HttpResponse("Erro: Nenhum cliente encontrado para simulação.", status=400)
            if not restaurante:
                return HttpResponse("Erro: Nenhum restaurante encontrado para simulação.", status=400)
            itens_carrinho = [
                {'produto_id': 1, 'quantidade': 2},
                {'produto_id': 2, 'quantidade': 1},
            ]
            metodo_pagamento = 'Pix' 

            novo_pedido = pedido_service.create_pedido_with_items(
                cliente=cliente,
                restaurante=restaurante,
                itens_carrinho=itens_carrinho,
                metodo_pagamento=metodo_pagamento
            )
            return HttpResponse(f"Pedido #{novo_pedido.id} criado com sucesso e pagamento registrado!")
        except Produto.DoesNotExist:
            return HttpResponse("Erro: Um dos produtos no carrinho não foi encontrado.", status=400)
        except Exception as e:
            return HttpResponse(f"Erro ao criar pedido: {e}", status=400)
    

    return render(request, 'criar_pedido_form.html') 
def sobre_nos(request):
    return render(request, 'sobre_nos.html')

def horario(request):
    return render(request, 'horario.html')

def avaliacoes(request):
    return render(request, 'avaliacoes.html')
def pedido(request):
    return render(request, 'pedido.html')

def contato(request):
    return render(request, 'contato.html')

def cadastro_page(request):
    return render(request, 'cadastro_page.html')



