"""Modelo Imagem."""


class Imagem:
    def __init__(self, caminho_pasta: str, descricao: str = "", id: int | None = None):
        self.id = id
        self.caminho_pasta = caminho_pasta
        self.descricao = descricao

    def obter_caminho(self) -> str:
        return self.caminho_pasta

    def __str__(self) -> str:
        return self.descricao or self.caminho_pasta
