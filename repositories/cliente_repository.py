"""Repositório de Cliente."""

from database.connection import get_connection
from models.cliente import Cliente


class ClienteRepository:
    def criar(self, cliente):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (nome, telefone, email, senha, tipo) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (cliente.nome, cliente.telefone, cliente.email, cliente.senha, "cliente"),
        )
        usuario_id = cur.fetchone()[0]
        cur.execute("INSERT INTO clientes (id) VALUES (%s)", (usuario_id,))
        conn.commit()
        cur.close()
        conn.close()
        return usuario_id

    def listar(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT u.id, u.nome, u.telefone, u.email, u.senha
            FROM usuarios u
            JOIN clientes c ON c.id = u.id
            ORDER BY u.nome
            """
        )
        clientes = [Cliente(id=row[0], nome=row[1], telefone=row[2], email=row[3], senha=row[4]) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return clientes

    def buscar_por_id(self, cliente_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT u.id, u.nome, u.telefone, u.email, u.senha
            FROM usuarios u
            JOIN clientes c ON c.id = u.id
            WHERE u.id = %s
            """,
            (cliente_id,),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        return Cliente(id=row[0], nome=row[1], telefone=row[2], email=row[3], senha=row[4])

    def atualizar(self, cliente):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuarios SET nome = %s, telefone = %s, email = %s, senha = COALESCE(NULLIF(%s, ''), senha) WHERE id = %s",
            (cliente.nome, cliente.telefone, cliente.email, cliente.senha, cliente.id),
        )
        conn.commit()
        cur.close()
        conn.close()

    def excluir(self, cliente_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id = %s", (cliente_id,))
        conn.commit()
        cur.close()
        conn.close()
