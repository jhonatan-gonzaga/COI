"""Serviço de Avaliação."""

from models.avaliacao import Avaliacao
from repositories.avaliacao_repository import AvaliacaoRepository


class AvaliacaoService:
    def __init__(self):
        self.repository = AvaliacaoRepository()

    def criar_avaliacao(self, dados):
        avaliacao = Avaliacao(nota=dados["nota"], comentario=dados["comentario"])
        if not avaliacao.validar_nota():
            raise ValueError("A nota deve estar entre 1 e 5.")
        if self.repository.existe_por_servico(dados["servico_id"]):
            raise ValueError("Este serviço já foi avaliado.")
        return self.repository.criar(dados)

    def listar_avaliacoes(self):
        return self.repository.listar()

    def listar_por_profissional(self, profissional_id):
        return self.repository.listar_por_profissional(profissional_id)

    def existe_por_servico(self, servico_id):
        return self.repository.existe_por_servico(servico_id)
