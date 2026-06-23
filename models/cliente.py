"""Modelo Cliente."""

from models.usuario import Usuario


class Cliente(Usuario):
    def solicitar_servico(self, descricao: str) -> str:
        return f"Solicitação criada: {descricao}"

    def avaliar_servico(self, nota: int, comentario: str) -> dict:
        return {"nota": nota, "comentario": comentario}

    def get_tipo(self) -> str:
        return "Cliente"
