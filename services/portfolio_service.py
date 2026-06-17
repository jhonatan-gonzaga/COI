"""Serviço de portfólio do profissional."""

from repositories.imagem_repository import ImagemRepository


class PortfolioService:
    def __init__(self):
        self.repository = ImagemRepository()

    def adicionar_imagem(self, profissional_id, caminho_pasta, descricao):
        return self.repository.criar(profissional_id, caminho_pasta, descricao)

    def listar_imagens(self, profissional_id):
        return self.repository.listar_por_profissional(profissional_id)

    def listar_imagens_profissional(self, profissional_id):
        return self.repository.listar_por_profissional(profissional_id)

    def buscar_imagem_do_profissional(self, imagem_id, profissional_id):
        return self.repository.buscar_do_profissional(imagem_id, profissional_id)

    def excluir_imagem(self, imagem_id, profissional_id):
        return self.repository.excluir_do_profissional(imagem_id, profissional_id)
