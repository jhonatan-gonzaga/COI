"""Modelo Servico."""


class Servico:
    STATUS_AGUARDANDO = "AGUARDANDO"
    STATUS_EM_ANDAMENTO = "EM_ANDAMENTO"
    STATUS_CONCLUIDO = "CONCLUIDO"
    STATUS_CANCELADO = "CANCELADO"

    def __init__(
        self,
        descricao: str,
        data_prevista,
        valor,
        status: str,
        cliente,
        profissional,
        endereco,
        id: int | None = None,
    ):
        self.id = id
        self.descricao = descricao
        self.data_prevista = data_prevista
        self.valor = float(valor)
        self.status = status
        self.cliente = cliente
        self.profissional = profissional
        self.endereco = endereco

    def concluir(self) -> None:
        self.status = self.STATUS_CONCLUIDO

    def cancelar(self) -> None:
        self.status = self.STATUS_CANCELADO

    def alterar_status(self, novo_status: str) -> None:
        self.status = novo_status

    def calcular_valor_final(self) -> float:
        return self.valor

    def __str__(self) -> str:
        return f"{self.descricao} - {self.status}"
