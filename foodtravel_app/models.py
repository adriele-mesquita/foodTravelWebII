from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Usuário")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    email = models.EmailField(unique=True, verbose_name="Email")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome


class EnderecoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos', verbose_name="Cliente")
    rua = models.CharField(max_length=200, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=50, verbose_name="Estado")
    cep = models.CharField(max_length=10, verbose_name="CEP")

    class Meta:
        verbose_name = "Endereço do Cliente"
        verbose_name_plural = "Endereços dos Clientes"

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"


class Restaurante(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Restaurante")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"

    def __str__(self):
        return self.nome


class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    class Meta:
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produtos"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='produtos', verbose_name="Restaurante")
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em Preparo', 'Em Preparo'),
        ('Em Entrega', 'Em Entrega'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos', verbose_name="Cliente")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='pedidos', verbose_name="Restaurante")
    data_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pedido")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente', verbose_name="Status")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Total")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens', verbose_name="Pedido")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no Pedido #{self.pedido.id}"


class Avaliacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name="Cliente")
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='avaliacoes', verbose_name="Restaurante")
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Nota (1-5)") 
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentário")
    data_avaliacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ('cliente', 'restaurante') 

    def __str__(self):
        return f"Avaliação de {self.cliente.nome} para {self.restaurante.nome} - Nota: {self.nota}"


class Funcionario(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='funcionario_perfil', verbose_name="Usuário")
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(unique=True, verbose_name="Email")
    data_contratacao = models.DateField(auto_now_add=True, verbose_name="Data de Contratação")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.nome


class Pagamento(models.Model):
    METODO_CHOICES = [
        ('Cartao Credito', 'Cartão de Crédito'),
        ('Cartao Debito', 'Cartão de Débito'),
        ('Dinheiro', 'Dinheiro'),
        ('Pix', 'Pix'),
        ('Outro', 'Outro'),
    ]
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='pagamento', verbose_name="Pedido")
    metodo_pagamento = models.CharField(max_length=50, choices=METODO_CHOICES, verbose_name="Método de Pagamento")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago")
    data_pagamento = models.DateTimeField(auto_now_add=True, verbose_name="Data do Pagamento")
    confirmado = models.BooleanField(default=False, verbose_name="Confirmado")
    transacao_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID da Transação")

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

    def __str__(self):
        return f"Pagamento do Pedido #{self.pedido.id} - {self.metodo_pagamento}"