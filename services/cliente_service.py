"""Serviço de Cliente."""

from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def criar_cliente(self, nome, telefone, email, senha=""):
        cliente = Cliente(nome=nome, telefone=telefone, email=email, senha=senha)
        return self.repository.criar(cliente)

    def listar_clientes(self):
        return self.repository.listar()

    def buscar_cliente(self, cliente_id):
        return self.repository.buscar_por_id(cliente_id)

    def atualizar_cliente(self, cliente_id, nome, telefone, email, senha=""):
        cliente = Cliente(id=cliente_id, nome=nome, telefone=telefone, email=email, senha=senha)
        self.repository.atualizar(cliente)

    def excluir_cliente(self, cliente_id):
        self.repository.excluir(cliente_id)
