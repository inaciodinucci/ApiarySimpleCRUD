import flet as ft

def criar_campo_texto(rotulo, largura=300):
    return ft.TextField(
        label=rotulo,
        width=largura,
        border_color=ft.colors.BLUE_400
    )