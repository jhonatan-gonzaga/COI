"""Repositório de autenticação de usuários."""

from database.connection import get_connection


class UsuarioRepository:

    #autentica o usuário pegando seus dados caso a senha e o email estejam corretos.
    def autenticar(self, email, senha):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, nome, telefone, email, tipo
            FROM usuarios
            WHERE email = %s AND senha = %s
            """,
            (email, senha),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        return {
            "id": row[0],
            "nome": row[1],
            "telefone": row[2],
            "email": row[3],
            "tipo": row[4],
        }
