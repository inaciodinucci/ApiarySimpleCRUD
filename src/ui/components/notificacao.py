import flet as ft

def mostrar_sucesso(pagina: ft.Page, mensagem: str):
    pagina.show_snack_bar(
        ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=ft.colors.GREEN_400,
            action="OK"
        )
    )

def mostrar_erro(pagina: ft.Page, mensagem: str):
    pagina.show_snack_bar(
        ft.SnackBar(
            content=ft.Text(f"Erro: {mensagem}"),
            bgcolor=ft.colors.RED_400,
            action="OK"
        )
    )