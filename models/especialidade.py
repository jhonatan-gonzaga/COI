"""Modelo Especialidade."""


class Especialidade:
    def __init__(self, nome: str, descricao: str = "", id: int | None = None):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def __str__(self) -> str:
        return self.nome
