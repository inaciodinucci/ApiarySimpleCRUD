import flet as ft
from src.models.produtor import Produtor

def view(page: ft.Page):
    def show_error(message: str):
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"Erro: {message}"),
                bgcolor=ft.colors.RED_400,
                action="OK",
            )
        )

    def show_success(message: str):
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.colors.GREEN_400,
                action="OK",
            )
        )

    # Campos do formulário
    nome = ft.TextField(label="Nome", width=300, border_color=ft.colors.BLUE_400)
    endereco = ft.TextField(label="Endereço", width=300, border_color=ft.colors.BLUE_400)
    telefone = ft.TextField(label="Telefone", width=300, border_color=ft.colors.BLUE_400)
    email = ft.TextField(label="Email", width=300, border_color=ft.colors.BLUE_400)
    
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
        rows=[],
        border=ft.border.all(2, ft.colors.BLUE_400),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(3, ft.colors.BLUE_100),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.BLUE_100),
    )

    def atualizar_tabela():
        try:
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
        except Exception as error:
            show_error(f"Erro ao carregar produtores: {str(error)}")

    def salvar_produtor(e):
        try:
            if not nome.value or not endereco.value or not telefone.value or not email.value:
                show_error("Todos os campos são obrigatórios!")
                return

            produtor = Produtor(
                nome=nome.value,
                endereco=endereco.value,
                telefone=telefone.value,
                email=email.value
            )
            produtor.salvar()
            limpar_campos()
            atualizar_tabela()
            show_success("Produtor salvo com sucesso!")
        except Exception as error:
            show_error(f"Erro ao salvar produtor: {str(error)}")

    def deletar_produtor(id):
        try:
            Produtor.deletar(id)
            atualizar_tabela()
            show_success("Produtor deletado com sucesso!")
        except Exception as error:
            show_error(f"Erro ao deletar produtor: {str(error)}")

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
                                ft.Text("Cadastro de Produtores", 
                                       size=20, 
                                       weight=ft.FontWeight.BOLD,
                                       color=ft.colors.BLUE_900),
                                ft.Column([nome, endereco, telefone, email],
                                        spacing=10),
                                ft.ElevatedButton(
                                    "Salvar",
                                    on_click=salvar_produtor,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.BLUE_400,
                                    )
                                ),
                            ],
                            spacing=20,
                        ),
                        padding=20,
                    )
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Lista de Produtores",
                                       size=20,
                                       weight=ft.FontWeight.BOLD,
                                       color=ft.colors.BLUE_900),
                                tabela,
                            ],
                            spacing=20,
                        ),
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