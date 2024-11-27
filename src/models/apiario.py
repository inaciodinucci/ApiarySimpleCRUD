from dataclasses import dataclass
from src.database.config import get_connection

@dataclass
class Apiario:
    id: int = None
    localizacao: str = ""
    tamanho: float = 0.0
    floracao: str = ""
    produtor_id: int = None

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            sql = """INSERT INTO apiario (localizacao, tamanho, floracao, produtor_id) 
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (self.localizacao, self.tamanho, self.floracao, 
                               self.produtor_id))
            self.id = cursor.lastrowid
        else:
            sql = """UPDATE apiario SET localizacao=%s, tamanho=%s, floracao=%s, 
                     produtor_id=%s WHERE id=%s"""
            cursor.execute(sql, (self.localizacao, self.tamanho, self.floracao, 
                               self.produtor_id, self.id))
        
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apiario")
        apiarios = []
        for row in cursor.fetchall():
            apiario = Apiario(id=row[0], localizacao=row[1], tamanho=row[2],
                            floracao=row[3], produtor_id=row[4])
            apiarios.append(apiario)
        cursor.close()
        conn.close()
        return apiarios

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM apiario WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()