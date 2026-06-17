"""Repositório de Imagem/Portfólio."""

from database.connection import get_connection


class ImagemRepository:
    def criar(self, profissional_id, caminho_pasta, descricao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO imagens (caminho_pasta, descricao, profissional_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (caminho_pasta, descricao, profissional_id),
        )
        imagem_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return imagem_id

    def listar_por_profissional(self, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, regexp_replace(caminho_pasta, '^uploads/', ''), descricao, profissional_id
            FROM imagens
            WHERE profissional_id = %s
            ORDER BY id DESC
            """,
            (profissional_id,),
        )
        imagens = [
            {
                "id": row[0],
                "caminho_pasta": row[1],
                "descricao": row[2],
                "profissional_id": row[3],
            }
            for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return imagens

    def buscar_do_profissional(self, imagem_id, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, regexp_replace(caminho_pasta, '^uploads/', ''), descricao, profissional_id
            FROM imagens
            WHERE id = %s AND profissional_id = %s
            """,
            (imagem_id, profissional_id),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return None
        return {
            "id": row[0],
            "caminho_pasta": row[1],
            "descricao": row[2],
            "profissional_id": row[3],
        }

    def excluir_do_profissional(self, imagem_id, profissional_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM imagens WHERE id = %s AND profissional_id = %s",
            (imagem_id, profissional_id),
        )
        excluiu = cur.rowcount > 0
        conn.commit()
        cur.close()
        conn.close()
        return excluiu
