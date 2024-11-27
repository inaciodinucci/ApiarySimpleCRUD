from dataclasses import dataclass
from datetime import datetime
from src.database.config import get_connection

@dataclass
class Produtor:
    id: int = None
    nome: str = ""
    endereco: str = ""
    telefone: str = ""
    email: str = ""

    def salvar(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            sql = """INSERT INTO produtor (nome, endereco, telefone, email) 
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (self.nome, self.endereco, self.telefone, self.email))
            self.id = cursor.lastrowid
        else:
            sql = """UPDATE produtor SET nome=%s, endereco=%s, telefone=%s, email=%s 
                     WHERE id=%s"""
            cursor.execute(sql, (self.nome, self.endereco, self.telefone, self.email, self.id))
        
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtor")
        produtores = []
        for row in cursor.fetchall():
            produtor = Produtor(id=row[0], nome=row[1], endereco=row[2], 
                              telefone=row[3], email=row[4])
            produtores.append(produtor)
        cursor.close()
        conn.close()
        return produtores

    @staticmethod
    def deletar(id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtor WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()