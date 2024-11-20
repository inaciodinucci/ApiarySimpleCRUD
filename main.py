import flet as ft
from interface import ApiarioInterface

def main(page: ft.Page):
    ApiarioInterface(page)

ft.app(target=main)