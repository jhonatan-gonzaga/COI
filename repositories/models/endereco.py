"""Modelo Endereco."""


class Endereco:
    def __init__(self, rua: str, numero: str, bairro: str):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro

    def formatar(self) -> str:
        return f"{self.rua}, {self.numero} - {self.bairro}"

    def __str__(self) -> str:
        return self.formatar()
