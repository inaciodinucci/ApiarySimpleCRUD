from dataclasses import dataclass
from datetime import date
from src.database.config import get_connection

@dataclass
class Colmeia:
    id: int = None
    numero_abelhas: int = 0
    tipo_abelhas: str = ""
    data_instalacao: date = None
    apiario_id: int = None

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            sql = """INSERT INTO colmeia (numero_abelhas, tipo_abelhas, data_instalacao, 
                     apiario_id) VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (self.numero_abelhas, self.tipo_abelhas,
                               self.data_instalacao, self.apiario_id))
            self.id = cursor.lastrowid
        else:
            sql = """UPDATE colmeia SET numero_abelhas=%s, tipo_abelhas=%s, 
                     data_instalacao=%s, apiario_id=%s WHERE id=%s"""
            cursor.execute(sql, (self.numero_abelhas, self.tipo_abelhas,
                               self.data_instalacao, self.apiario_id, self.id))
        
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM colmeia")
        colmeias = []
        for row in cursor.fetchall():
            colmeia = Colmeia(id=row[0], numero_abelhas=row[1], tipo_abelhas=row[2],
                             data_instalacao=row[3], apiario_id=row[4])
            colmeias.append(colmeia)
        cursor.close()
        conn.close()
        return colmeias

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM colmeia WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()