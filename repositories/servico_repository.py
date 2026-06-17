"""Repositório de Serviço."""

from database.connection import get_connection


class ServicoRepository:
    def criar(self, dados):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO enderecos (rua, numero, bairro) VALUES (%s, %s, %s) RETURNING id",
            (dados["rua"], dados["numero"], dados["bairro"]),
        )
        endereco_id = cur.fetchone()[0]
        cur.execute(
            """
            INSERT INTO servicos
            (descricao, data_prevista, valor, status, cliente_id, profissional_id, endereco_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                dados["descricao"],
                dados["data_prevista"],
                dados["valor"],
                dados.get("status", "AGUARDANDO"),
                dados["cliente_id"],
                dados.get("profissional_id") or None,
                endereco_id,
            ),
        )
        servico_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return servico_id

    def listar(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT s.id, s.descricao, s.data_prevista, s.valor, s.status,
                   s.cliente_id, s.profissional_id, s.endereco_id,
                   uc.nome AS cliente, up.nome AS profissional,
                   e.rua, e.numero, e.bairro,
                   CASE WHEN a.id IS NULL THEN FALSE ELSE TRUE END AS avaliado
            FROM servicos s
            JOIN clientes c ON c.id = s.cliente_id
            JOIN usuarios uc ON uc.id = c.id
            LEFT JOIN profissionais p ON p.id = s.profissional_id
            LEFT JOIN usuarios up ON up.id = p.id
            JOIN enderecos e ON e.id = s.endereco_id
            LEFT JOIN avaliacoes a ON a.servico_id = s.id
            ORDER BY s.id DESC
            """
        )
        colunas = [desc[0] for desc in cur.description]
        servicos = [dict(zip(colunas, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return servicos

    def listar_por_cliente(self, cliente_id):
        servicos = self.listar()
        return [servico for servico in servicos if servico["cliente_id"] == int(cliente_id)]

    def listar_por_profissional(self, profissional_id):
        servicos = self.listar()
        return [servico for servico in servicos if servico["profissional_id"] == int(profissional_id)]

    def listar_pedidos_profissional(self, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT s.id, s.descricao, s.data_prevista, s.valor, s.status,
                   s.cliente_id, s.profissional_id, uc.nome AS cliente,
                   e.rua, e.numero, e.bairro
            FROM servicos s
            JOIN usuarios uc ON uc.id = s.cliente_id
            JOIN enderecos e ON e.id = s.endereco_id
            WHERE s.profissional_id = %s AND s.status IN ('AGUARDANDO', 'EM_ANDAMENTO')
            ORDER BY s.id DESC
            """,
            (profissional_id,),
        )
        colunas = [desc[0] for desc in cur.description]
        servicos = [dict(zip(colunas, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return servicos

    def buscar_por_id(self, servico_id):
        servicos = [s for s in self.listar() if s["id"] == int(servico_id)]
        return servicos[0] if servicos else None

    def atualizar(self, servico_id, dados):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE servicos
            SET descricao = %s, data_prevista = %s, valor = %s, status = %s,
                cliente_id = %s, profissional_id = %s
            WHERE id = %s
            """,
            (
                dados["descricao"],
                dados["data_prevista"],
                dados["valor"],
                dados["status"],
                dados["cliente_id"],
                dados.get("profissional_id") or None,
                servico_id,
            ),
        )
        cur.execute(
            """
            UPDATE enderecos e
            SET rua = %s, numero = %s, bairro = %s
            FROM servicos s
            WHERE s.endereco_id = e.id AND s.id = %s
            """,
            (dados["rua"], dados["numero"], dados["bairro"], servico_id),
        )
        conn.commit()
        cur.close()
        conn.close()

    def alterar_status(self, servico_id, status):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE servicos SET status = %s WHERE id = %s", (status, servico_id))
        conn.commit()
        cur.close()
        conn.close()

    def pertence_ao_cliente(self, servico_id, cliente_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM servicos WHERE id = %s AND cliente_id = %s",
            (servico_id, cliente_id),
        )
        existe = cur.fetchone() is not None
        cur.close()
        conn.close()
        return existe

    def excluir(self, servico_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM servicos WHERE id = %s", (servico_id,))
        conn.commit()
        cur.close()
        conn.close()
