import flet as ft

def criar_botoes_acao(ao_salvar, ao_cancelar=None):
    botao_salvar = ft.ElevatedButton(
        "Salvar",
        on_click=ao_salvar,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_400,
        )
    )
    
    botao_cancelar = ft.ElevatedButton(
        "Cancelar",
        on_click=ao_cancelar,
        visible=False if not ao_cancelar else True
    )
    
    return botao_salvar, botao_cancelar