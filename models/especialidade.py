"""Modelo Especialidade."""


class Especialidade:
    def __init__(self, nome, descricao="", id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
