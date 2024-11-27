import flet as ft

def criar_cartao_formulario(titulo, conteudo):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        titulo,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_900
                    ),
                    *conteudo
                ],
                spacing=20,
            ),
            padding=20,
        )
    )