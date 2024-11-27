import flet as ft
from src.models.apiario import Apiario
from src.models.produtor import Produtor

def view(page: ft.Page):
    # Campos do formulário
    localizacao = ft.TextField(label="Localização", width=300)
    tamanho = ft.TextField(label="Tamanho", width=300)
    floracao = ft.TextField(label="Floração", width=300)
    
    # Dropdown para selecionar produtor
    produtores = [ft.dropdown.Option(str(p.id), p.nome) 
                  for p in Produtor.buscar_todos()]
    produtor_dd = ft.Dropdown(
        label="Produtor",
        width=300,
        options=produtores
    )

    # DataTable para listar apiários
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Localização")),
            ft.DataColumn(ft.Text("Tamanho")),
            ft.DataColumn(ft.Text("Floração")),
            ft.DataColumn(ft.Text("Produtor")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def atualizar_tabela():
        tabela.rows.clear()
        for a in Apiario.buscar_todos():
            produtor = next((p for p in Produtor.buscar_todos() 
                           if p.id == a.produtor_id), None)
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(a.id)),
                        ft.DataCell(ft.Text(a.localizacao)),
                        ft.DataCell(ft.Text(a.tamanho)),
                        ft.DataCell(ft.Text(a.floracao)),
                        ft.DataCell(ft.Text(produtor.nome if produtor else "")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, id=a.id: deletar_apiario(id)
                                )
                            ])
                        ),
                    ]
                )
            )
        page.update()

    def salvar_apiario(e):
        apiario = Apiario(
            localizacao=localizacao.value,
            tamanho=float(tamanho.value),
            floracao=floracao.value,
            produtor_id=int(produtor_dd.value)
        )
        apiario.salvar()
        limpar_campos()
        atualizar_tabela()

    def deletar_apiario(id):
        Apiario.deletar(id)
        atualizar_tabela()

    def limpar_campos():
        localizacao.value = ""
        tamanho.value = ""
        floracao.value = ""
        produtor_dd.value = None
        page.update()

    # Layout
    content = ft.Column(
        [
            ft.Text("Cadastro de Apiários", size=20, weight=ft.FontWeight.BOLD),
            ft.Column([localizacao, tamanho, floracao, produtor_dd]),
            ft.ElevatedButton("Salvar", on_click=salvar_apiario),
            ft.Divider(),
            tabela
        ],
        scroll=ft.ScrollMode.AUTO
    )

    atualizar_tabela()
    return content