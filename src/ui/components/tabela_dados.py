import flet as ft

def criar_tabela_dados(colunas):
    return ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in colunas],
        rows=[],
        border=ft.border.all(2, ft.colors.BLUE_400),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(3, ft.colors.BLUE_100),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.BLUE_100),
    )