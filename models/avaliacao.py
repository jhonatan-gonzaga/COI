"""Modelo Avaliacao."""


class Avaliacao:
    def __init__(self, nota: int, comentario: str, id: int | None = None):
        self.id = id
        self.nota = int(nota)
        self.comentario = comentario

    def validar_nota(self) -> bool:
        return 1 <= self.nota <= 5

    def __str__(self) -> str:
        return f"Nota {self.nota}: {self.comentario}"
