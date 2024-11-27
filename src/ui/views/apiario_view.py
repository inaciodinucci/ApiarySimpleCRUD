import flet as ft
from src.models.apiario import Apiario
from src.models.produtor import Produtor

def view(page: ft.Page):
    # Estado para controlar modo de edição
    apiario_em_edicao = None
    
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
    
    # Botões
    btn_salvar = ft.ElevatedButton("Salvar", on_click=lambda e: salvar_apiario(e))
    btn_cancelar = ft.ElevatedButton(
        "Cancelar",
        on_click=lambda e: cancelar_edicao(),
        visible=False
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
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE_400,
                                    tooltip="Editar",
                                    on_click=lambda e, a=a: iniciar_edicao(a)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED_400,
                                    tooltip="Deletar",
                                    on_click=lambda e, id=a.id: deletar_apiario(id)
                                )
                            ])
                        ),
                    ]
                )
            )
        page.update()

    def iniciar_edicao(apiario):
        nonlocal apiario_em_edicao
        apiario_em_edicao = apiario
        
        # Preencher campos com dados atuais
        localizacao.value = apiario.localizacao
        tamanho.value = str(apiario.tamanho)
        floracao.value = apiario.floracao
        produtor_dd.value = str(apiario.produtor_id)
        
        # Atualizar interface
        btn_salvar.text = "Atualizar"
        btn_cancelar.visible = True
        page.update()

    def cancelar_edicao():
        nonlocal apiario_em_edicao
        apiario_em_edicao = None
        limpar_campos()
        btn_salvar.text = "Salvar"
        btn_cancelar.visible = False
        page.update()

    def salvar_apiario(e):
        nonlocal apiario_em_edicao
        
        if not all([localizacao.value, tamanho.value, floracao.value, produtor_dd.value]):
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Todos os campos são obrigatórios!"),
                    bgcolor=ft.colors.RED_400
                )
            )
            return
            
        try:
            apiario = Apiario(
                id=apiario_em_edicao.id if apiario_em_edicao else None,
                localizacao=localizacao.value,
                tamanho=float(tamanho.value),
                floracao=floracao.value,
                produtor_id=int(produtor_dd.value)
            )
            apiario.salvar()
            limpar_campos()
            atualizar_tabela()
            cancelar_edicao()
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Apiário salvo com sucesso!"),
                    bgcolor=ft.colors.GREEN_400
                )
            )
        except ValueError:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Tamanho deve ser um número válido!"),
                    bgcolor=ft.colors.RED_400
                )
            )
        except Exception as error:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao salvar: {str(error)}"),
                    bgcolor=ft.colors.RED_400
                )
            )

    def deletar_apiario(id):
        try:
            Apiario.deletar(id)
            atualizar_tabela()
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Apiário deletado com sucesso!"),
                    bgcolor=ft.colors.GREEN_400
                )
            )
        except Exception as error:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao deletar: {str(error)}"),
                    bgcolor=ft.colors.RED_400
                )
            )

    def limpar_campos():
        localizacao.value = ""
        tamanho.value = ""
        floracao.value = ""
        produtor_dd.value = None
        page.update()

    # Layout
    content = ft.Container(
        content=ft.Column(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Cadastro de Apiários",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLUE_900
                                ),
                                ft.Column(
                                    [localizacao, tamanho, floracao, produtor_dd],
                                    spacing=10
                                ),
                                ft.Row(
                                    [btn_salvar, btn_cancelar],
                                    spacing=10
                                ),
                            ],
                            spacing=20,
                        ),
                        padding=20,
                    )
                ),
                ft.Card(
                    content=ft.Container(
                        content=tabela,
                        padding=20,
                    )
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
        ),
        padding=20,
    )

    atualizar_tabela()
    return content