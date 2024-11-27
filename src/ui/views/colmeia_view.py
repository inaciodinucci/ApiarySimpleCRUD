import flet as ft
from datetime import date
from src.models.colmeia import Colmeia
from src.models.apiario import Apiario

def view(page: ft.Page):
    # Campos do formulário
    numero_abelhas = ft.TextField(label="Número de Abelhas", width=300)
    tipo_abelhas = ft.TextField(label="Tipo de Abelhas", width=300)
    data_instalacao = ft.TextField(
        label="Data de Instalação (YYYY-MM-DD)",
        width=300
    )
    
    # Dropdown para selecionar apiário
    apiarios = [ft.dropdown.Option(str(a.id), f"Apiário {a.id} - {a.localizacao}") 
                for a in Apiario.buscar_todos()]
    apiario_dd = ft.Dropdown(
        label="Apiário",
        width=300,
        options=apiarios
    )

    # DataTable para listar colmeias
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nº Abelhas")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Instalação")),
            ft.DataColumn(ft.Text("Apiário")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def atualizar_tabela():
        tabela.rows.clear()
        for c in Colmeia.buscar_todos():
            apiario = next((a for a in Apiario.buscar_todos() 
                          if a.id == c.apiario_id), None)
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(c.id)),
                        ft.DataCell(ft.Text(c.numero_abelhas)),
                        ft.DataCell(ft.Text(c.tipo_abelhas)),
                        ft.DataCell(ft.Text(c.data_instalacao)),
                        ft.DataCell(ft.Text(
                            f"Apiário {apiario.id}" if apiario else ""
                        )),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, id=c.id: deletar_colmeia(id)
                                )
                            ])
                        ),
                    ]
                )
            )
        page.update()

    def salvar_colmeia(e):
        try:
            colmeia = Colmeia(
                numero_abelhas=int(numero_abelhas.value),
                tipo_abelhas=tipo_abelhas.value,
                data_instalacao=date.fromisoformat(data_instalacao.value),
                apiario_id=int(apiario_dd.value)
            )
            colmeia.salvar()
            limpar_campos()
            atualizar_tabela()
        except ValueError as error:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Erro: {str(error)}"))
            )

    def deletar_colmeia(id):
        Colmeia.deletar(id)
        atualizar_tabela()

    def limpar_campos():
        numero_abelhas.value = ""
        tipo_abelhas.value = ""
        data_instalacao.value = ""
        apiario_dd.value = None
        page.update()

    # Layout
    content = ft.Column(
        [
            ft.Text("Cadastro de Colmeias", size=20, weight=ft.FontWeight.BOLD),
            ft.Column([numero_abelhas, tipo_abelhas, data_instalacao, apiario_dd]),
            ft.ElevatedButton("Salvar", on_click=salvar_colmeia),
            ft.Divider(),
            tabela
        ],
        scroll=ft.ScrollMode.AUTO
    )

    atualizar_tabela()
    return content