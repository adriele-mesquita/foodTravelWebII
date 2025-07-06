from ..models import Produto, CategoriaProduto, Restaurante
from django.db.models import QuerySet

class ProdutoService:
   
    def get_all_produtos(self) -> QuerySet[Produto]:
        return Produto.objects.filter(disponivel=True)

    def get_produtos_by_categoria(self, categoria_id: int) -> QuerySet[Produto]:
        return Produto.objects.filter(categoria__id=categoria_id, disponivel=True)

    def get_produto_by_id(self, produto_id: int) -> Produto | None:
        try:
            return Produto.objects.get(id=produto_id, disponivel=True)
        except Produto.DoesNotExist:
            return None

    def create_produto(self, restaurante: Restaurante, categoria: CategoriaProduto, nome: str, descricao: str, preco: float) -> Produto:
        produto = Produto.objects.create(
            restaurante=restaurante,
            categoria=categoria,
            nome=nome,
            descricao=descricao,
            preco=preco,
            disponivel=True
        )
        return produto

    def update_produto_preco(self, produto_id: int, novo_preco: float) -> Produto | None:
        produto = self.get_produto_by_id(produto_id)
        if produto:
            produto.preco = novo_preco
            produto.save()
        return produto

    def delete_produto(self, produto_id: int) -> bool:
        produto = self.get_produto_by_id(produto_id)
        if produto:
            produto.delete()
            return True
        return False
