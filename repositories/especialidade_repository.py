"""Repositório de Especialidade."""

from database.connection import get_connection

class EspecialidadeRepository:
    #lista todas especialidades, seus nomes, ids e descrições.
    def listar(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, descricao FROM especialidades ORDER BY nome")
        especialidades = [
            {"id": row[0], "nome": row[1], "descricao": row[2]}
            for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return especialidades
