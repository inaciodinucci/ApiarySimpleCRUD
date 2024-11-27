import flet as ft
from datetime import date

def criar_seletor_data(pagina: ft.Page, ao_mudar=None):
    data_selecionada = date.today()
    
    def manipular_mudanca_data(e):
        if e.control.value and ao_mudar:
            ao_mudar(e.control.value)
    
    seletor_data = ft.DatePicker(
        on_change=manipular_mudanca_data,
        first_date=date(2020, 1, 1),
        last_date=date(2030, 12, 31)
    )
    
    pagina.overlay.append(seletor_data)
    
    campo_data = ft.TextField(
        label="Data de Instalação",
        width=300,
        read_only=True,
        value=data_selecionada.strftime("%d/%m/%Y")
    )
    
    botao_data = ft.IconButton(
        icon=ft.icons.CALENDAR_TODAY,
        tooltip="Selecionar Data",
        on_click=lambda _: seletor_data.pick_date()
    )
    
    return ft.Row(
        [campo_data, botao_data],
        spacing=0
    ), seletor_data, campo_data