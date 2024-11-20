import flet as ft
from database import Apiario

class ApiarioInterface:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Apiario()
        self.colmeia_atual = None
        self.setup_page()
        self.criar_componentes()
        self.criar_layout()
        self.atualizar_tabela()

    def setup_page(self):
        self.page.title = "Sistema de Gerenciamento de Apiário (NoSQL)"
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.padding = 20
        self.page.theme_mode = "light"

    def criar_componentes(self):
        self.identificacao = ft.TextField(label="Identificação da Colmeia", width=300)
        self.data_instalacao = ft.TextField(label="Data de Instalação (YYYY-MM-DD)", width=300)
        self.producao_mel = ft.TextField(label="Produção de Mel (kg)", width=300)
        self.estado_saude = ft.Dropdown(
            label="Estado de Saúde",
            width=300,
            options=[
                ft.dropdown.Option("Saudável"),
                ft.dropdown.Option("Requer Atenção"),
                ft.dropdown.Option("Crítico")
            ]
        )
        self.observacoes = ft.TextField(label="Observações", width=300, multiline=True)
        
        self.tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Identificação")),
                ft.DataColumn(ft.Text("Data Instalação")),
                ft.DataColumn(ft.Text("Produção Mel (kg)")),
                ft.DataColumn(ft.Text("Estado Saúde")),
                ft.DataColumn(ft.Text("Observações")),
                ft.DataColumn(ft.Text("Última Atualização")),
                ft.DataColumn(ft.Text("Ações"))
            ],
            rows=[]
        )

    def limpar_campos(self):
        self.colmeia_atual = None
        self.identificacao.value = ""
        self.data_instalacao.value = ""
        self.producao_mel.value = ""
        self.estado_saude.value = None
        self.observacoes.value = ""
        self.page.update()

    def salvar_colmeia(self, e):
        try:
            dados = {
                'identificacao': self.identificacao.value,
                'data_instalacao': self.data_instalacao.value,
                'producao_mel': self.producao_mel.value,
                'estado_saude': self.estado_saude.value,
                'observacoes': self.observacoes.value
            }

            if self.colmeia_atual:
                self.db.atualizar_colmeia(self.colmeia_atual, dados)
                mensagem = "Colmeia atualizada com sucesso!"
            else:
                self.db.adicionar_colmeia(**dados)
                mensagem = "Colmeia adicionada com sucesso!"

            self.limpar_campos()
            self.atualizar_tabela()
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(mensagem)))
        except Exception as erro:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Erro ao salvar colmeia: {str(erro)}")))

    def excluir_colmeia(self, e):
        try:
            self.db.excluir_colmeia(e.control.data)
            self.atualizar_tabela()
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Colmeia excluída com sucesso!")))
        except Exception as erro:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Erro ao excluir colmeia: {str(erro)}")))

    def carregar_colmeia(self, doc_id):
        colmeia = self.db.buscar_colmeia(doc_id)
        if colmeia:
            self.colmeia_atual = doc_id
            self.identificacao.value = colmeia['identificacao']
            self.data_instalacao.value = colmeia['data_instalacao']
            self.producao_mel.value = str(colmeia['producao_mel'])
            self.estado_saude.value = colmeia['estado_saude']
            self.observacoes.value = colmeia['observacoes']
            self.page.update()

    def atualizar_tabela(self):
        self.tabela.rows.clear()
        for colmeia in self.db.listar_colmeias():
            doc_id = colmeia.doc_id
            self.tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(doc_id))),
                        ft.DataCell(ft.Text(colmeia['identificacao'])),
                        ft.DataCell(ft.Text(colmeia['data_instalacao'])),
                        ft.DataCell(ft.Text(str(colmeia['producao_mel']))),
                        ft.DataCell(ft.Text(colmeia['estado_saude'])),
                        ft.DataCell(ft.Text(colmeia['observacoes'])),
                        ft.DataCell(ft.Text(colmeia['timestamp'].split('T')[0])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color="red",
                                        data=doc_id,
                                        on_click=self.excluir_colmeia
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        icon_color="blue",
                                        data=doc_id,
                                        on_click=lambda e: self.carregar_colmeia(e.control.data)
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        self.page.update()

    def criar_layout(self):
        self.page.add(
            ft.Text("Gerenciamento de Colmeias (NoSQL)", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Column([
                ft.Row([self.identificacao, self.data_instalacao]),
                ft.Row([self.producao_mel, self.estado_saude]),
                self.observacoes,
                ft.Row([
                    ft.ElevatedButton("Salvar Colmeia", on_click=self.salvar_colmeia),
                    ft.OutlinedButton("Limpar Campos", on_click=lambda _: self.limpar_campos())
                ]),
            ]),
            ft.Divider(),
            self.tabela
        )