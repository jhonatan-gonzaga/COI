"""Modelo ProfissionalAutonomo."""

from models.usuario import Usuario


class ProfissionalAutonomo(Usuario):
    def __init__(self, nome, telefone, email, senha="", especialidades=None, portfolio=None, id=None):
        super().__init__(nome, telefone, email, senha, id)
        self._especialidades = list(especialidades or [])
        self._portfolio = list(portfolio or [])

    @property
    def especialidades(self):
        return self._especialidades

    @especialidades.setter
    def especialidades(self, especialidades):
        self._especialidades = list(especialidades or [])

    @property
    def portfolio(self):
        return self._portfolio

    @portfolio.setter
    def portfolio(self, portfolio):
        self._portfolio = list(portfolio or [])

    def adicionar_especialidade(self, especialidade) -> None:
        if especialidade not in self._especialidades:
            self._especialidades.append(especialidade)

    def remover_especialidade(self, especialidade) -> None:
        if especialidade in self._especialidades:
            self._especialidades.remove(especialidade)

    def adicionar_imagem(self, imagem) -> None:
        if imagem not in self._portfolio:
            self._portfolio.append(imagem)

    def listar_portfolio(self) -> list:
        return list(self._portfolio)

    def get_tipo(self) -> str:
        return "Profissional Autônomo"
