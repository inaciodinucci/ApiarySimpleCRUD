from tinydb import TinyDB, Query
from datetime import datetime

class Apiario:
    def __init__(self):
        self.db = TinyDB('apiario.json')
        self.colmeias = self.db.table('colmeias')
        self.Colmeia = Query()

    def adicionar_colmeia(self, identificacao, data_instalacao, producao_mel, estado_saude, observacoes):
        colmeia = {
            'identificacao': identificacao,
            'data_instalacao': data_instalacao,
            'producao_mel': float(producao_mel),
            'estado_saude': estado_saude,
            'observacoes': observacoes,
            'timestamp': datetime.now().isoformat()
        }
        return self.colmeias.insert(colmeia)

    def listar_colmeias(self):
        return self.colmeias.all()

    def buscar_colmeia(self, doc_id):
        return self.colmeias.get(doc_id=doc_id)

    def excluir_colmeia(self, doc_id):
        self.colmeias.remove(doc_ids=[doc_id])

    def atualizar_colmeia(self, doc_id, dados):
        dados['timestamp'] = datetime.now().isoformat()
        self.colmeias.update(dados, doc_ids=[doc_id])