import flet as ft
from src.models.produtor import Produtor

def view(page: ft.Page):
    # Estado para controlar modo de edição
    produtor_em_edicao = None
    
    # Campos do formulário
    nome = ft.TextField(label="Nome", width=300)
    endereco = ft.TextField(label="Endereço", width=300)
    telefone = ft.TextField(label="Telefone", width=300)
    email = ft.TextField(label="Email", width=300)
    
    # Botões
    btn_salvar = ft.ElevatedButton("Salvar", on_click=lambda e: salvar_produtor(e))
    btn_cancelar = ft.ElevatedButton(
        "Cancelar",
        on_click=lambda e: cancelar_edicao(),
        visible=False
    )
    
    # DataTable para listar produtores
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Endereço")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def atualizar_tabela():
        tabela.rows.clear()
        for p in Produtor.buscar_todos():
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.id)),
                        ft.DataCell(ft.Text(p.nome)),
                        ft.DataCell(ft.Text(p.endereco)),
                        ft.DataCell(ft.Text(p.telefone)),
                        ft.DataCell(ft.Text(p.email)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE_400,
                                    tooltip="Editar",
                                    on_click=lambda e, p=p: iniciar_edicao(p)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED_400,
                                    tooltip="Deletar",
                                    on_click=lambda e, id=p.id: deletar_produtor(id)
                                )
                            ])
                        ),
                    ]
                )
            )
        page.update()

    def iniciar_edicao(produtor):
        nonlocal produtor_em_edicao
        produtor_em_edicao = produtor
        
        # Preencher campos com dados atuais
        nome.value = produtor.nome
        endereco.value = produtor.endereco
        telefone.value = produtor.telefone
        email.value = produtor.email
        
        # Atualizar interface
        btn_salvar.text = "Atualizar"
        btn_cancelar.visible = True
        page.update()

    def cancelar_edicao():
        nonlocal produtor_em_edicao
        produtor_em_edicao = None
        limpar_campos()
        btn_salvar.text = "Salvar"
        btn_cancelar.visible = False
        page.update()

    def salvar_produtor(e):
        nonlocal produtor_em_edicao
        
        if not all([nome.value, endereco.value, telefone.value, email.value]):
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Todos os campos são obrigatórios!"),
                    bgcolor=ft.colors.RED_400
                )
            )
            return
            
        produtor = Produtor(
            id=produtor_em_edicao.id if produtor_em_edicao else None,
            nome=nome.value,
            endereco=endereco.value,
            telefone=telefone.value,
            email=email.value
        )
        
        try:
            produtor.salvar()
            limpar_campos()
            atualizar_tabela()
            cancelar_edicao()
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Produtor salvo com sucesso!"),
                    bgcolor=ft.colors.GREEN_400
                )
            )
        except Exception as error:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao salvar: {str(error)}"),
                    bgcolor=ft.colors.RED_400
                )
            )

    def deletar_produtor(id):
        try:
            Produtor.deletar(id)
            atualizar_tabela()
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Produtor deletado com sucesso!"),
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
        nome.value = ""
        endereco.value = ""
        telefone.value = ""
        email.value = ""
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
                                    "Cadastro de Produtores",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLUE_900
                                ),
                                ft.Column([nome, endereco, telefone, email], spacing=10),
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