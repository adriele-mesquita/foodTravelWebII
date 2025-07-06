from ..models import Pedido, Cliente, Restaurante, Produto, ItemPedido, Pagamento
from django.db import transaction
from django.db.models import QuerySet

class PedidoService:
    def get_all_pedidos(self) -> QuerySet[Pedido]:
        return Pedido.objects.all().order_by('-data_pedido')

    def get_pedidos_by_cliente(self, cliente: Cliente) -> QuerySet[Pedido]:
        return Pedido.objects.filter(cliente=cliente).order_by('-data_pedido')

    def get_pedido_by_id(self, pedido_id: int) -> Pedido | None:
        try:
            return Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return None

    @transaction.atomic 
    def create_pedido_with_items(self, cliente: Cliente, restaurante: Restaurante, itens_carrinho: list[dict], metodo_pagamento: str) -> Pedido:
        if not itens_carrinho:
            raise ValueError("O carrinho não pode estar vazio para criar um pedido.")

        pedido = Pedido.objects.create(
            cliente=cliente,
            restaurante=restaurante,
            status='Pendente',
            valor_total=0.00 
        )
        total_pedido = 0

        for item_data in itens_carrinho:
            produto_id = item_data.get('produto_id')
            quantidade = item_data.get('quantidade')

            if not produto_id or not quantidade or quantidade <= 0:
                raise ValueError(f"Dados inválidos para o item do carrinho: {item_data}")

            produto = Produto.objects.get(id=produto_id)
            preco_unitario = produto.preco
            subtotal = preco_unitario * quantidade

            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal
            )
            total_pedido += subtotal

        pedido.valor_total = total_pedido
        pedido.save()

        Pagamento.objects.create(
            pedido=pedido,
            metodo_pagamento=metodo_pagamento,
            valor_pago=total_pedido,
            confirmado=True
        )

        return pedido

    def update_pedido_status(self, pedido_id: int, novo_status: str) -> Pedido | None:
        pedido = self.get_pedido_by_id(pedido_id)
        if pedido:
            pedido.status = novo_status
            pedido.save()
        return pedido
