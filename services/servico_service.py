"""Serviço de Serviço."""

from repositories.servico_repository import ServicoRepository


class ServicoService:
    def __init__(self):
        self.repository = ServicoRepository()

    def criar_servico(self, dados):
        return self.repository.criar(dados)

    def listar_servicos(self):
        return self.repository.listar()

    def buscar_servico(self, servico_id):
        return self.repository.buscar_por_id(servico_id)

    def listar_por_cliente(self, cliente_id):
        return self.repository.listar_por_cliente(cliente_id)

    def listar_por_profissional(self, profissional_id):
        return self.repository.listar_por_profissional(profissional_id)

    def listar_pedidos_profissional(self, profissional_id):
        return self.repository.listar_pedidos_profissional(profissional_id)

    def servico_pertence_ao_cliente(self, servico_id, cliente_id):
        return self.repository.pertence_ao_cliente(servico_id, cliente_id)

    def atualizar_servico(self, servico_id, dados):
        self.repository.atualizar(servico_id, dados)

    def alterar_status(self, servico_id, status):
        self.repository.alterar_status(servico_id, status)

    def excluir_servico(self, servico_id):
        self.repository.excluir(servico_id)
