"""Modelo Imagem."""


class Imagem:
    def __init__(self, caminho_pasta, descricao="", id=None):
        self.id = id
        self.caminho_pasta = caminho_pasta
        self.descricao = descricao
