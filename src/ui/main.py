import flet as ft
from src.ui.views import (
    produtor_view,
    apiario_view,
    colmeia_view
)

def main(page: ft.Page):
    page.title = "Gerenciador de Apiário"
    page.padding = 20
    page.theme_mode = "light"
    page.window_width = 1200
    page.window_height = 800

    # Container para conteúdo dinâmico
    content_area = ft.Container(
        content=ft.Column(
            [ft.Text("Bem-vindo ao Gerenciador de Apiário", size=32)],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        padding=20
    )

    def route_change(route):
        content_area.content = None
        if route == "/produtor":
            content_area.content = produtor_view.view(page)
        elif route == "/apiario":
            content_area.content = apiario_view.view(page)
        elif route == "/colmeia":
            content_area.content = colmeia_view.view(page)
        else:
            content_area.content = ft.Column(
                [
                    ft.Text("Bem-vindo ao Gerenciador de Apiário", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text("Selecione uma opção no menu lateral", size=16),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        page.update()

    # Menu Lateral
    rail = ft.NavigationRail(
        selected_index=None,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.PERSON,
                selected_icon=ft.icons.PERSON_OUTLINED,
                label="Produtores",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LANDSCAPE,
                selected_icon=ft.icons.LANDSCAPE_OUTLINED,
                label="Apiários",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.HIVE,
                selected_icon=ft.icons.HIVE_OUTLINED,
                label="Colmeias",
            ),
        ],
        on_change=lambda e: route_change(
            ["/produtor", "/apiario", "/colmeia"][e.control.selected_index]
        ),
    )

    # Layout Principal
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )

    route_change("/")