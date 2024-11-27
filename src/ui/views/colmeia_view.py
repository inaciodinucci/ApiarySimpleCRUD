import flet as ft
from datetime import date, datetime
from src.models.colmeia import Colmeia
from src.models.apiario import Apiario

def view(page: ft.Page):
    # Estado para controlar modo de edição
    colmeia_em_edicao = None
    
    # Campos do formulário
    numero_abelhas = ft.TextField(label="Número de Abelhas", width=300)
    tipo_abelhas = ft.TextField(label="Tipo de Abelhas", width=300)
    
    # Campo de data com DatePicker
    data_selecionada = date.today()
    
    def on_date_change(e):
        nonlocal data_selecionada
        if e.control.value:
            data_selecionada = e.control.value
            data_instalacao_display.value = data_selecionada.strftime("%d/%m/%Y")
            page.update()
    
    date_picker = ft.DatePicker(
        on_change=on_date_change,
        first_date=date(2020, 1, 1),
        last_date=date(2030, 12, 31)
    )
    
    page.overlay.append(date_picker)
    
    data_instalacao_display = ft.TextField(
        label="Data de Instalação",
        width=300,
        read_only=True,
        value=data_selecionada.strftime("%d/%m/%Y")
    )
    
    btn_date = ft.IconButton(
        icon=ft.icons.CALENDAR_TODAY,
        tooltip="Selecionar Data",
        on_click=lambda _: date_picker.pick_date()
    )
    
    data_container = ft.Row(
        [data_instalacao_display, btn_date],
        spacing=0
    )
    
    # Dropdown para selecionar apiário
    apiarios = [ft.dropdown.Option(str(a.id), f"Apiário {a.id} - {a.localizacao}") 
                for a in Apiario.buscar_todos()]
    apiario_dd = ft.Dropdown(
        label="Apiário",
        width=300,
        options=apiarios
    )
    
    # Botões
    btn_salvar = ft.ElevatedButton("Salvar", on_click=lambda e: salvar_colmeia(e))
    btn_cancelar = ft.ElevatedButton(
        "Cancelar",
        on_click=lambda e: cancelar_edicao(),
        visible=False
    )

    # DataTable para listar colmeias
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nº Abelhas")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Instalação")),
            ft.DataColumn(ft.Text("Apiário")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def atualizar_tabela():
        tabela.rows.clear()
        for c in Colmeia.buscar_todos():
            apiario = next((a for a in Apiario.buscar_todos() 
                          if a.id == c.apiario_id), None)
            # Converter a data para formato brasileiro
            data_formatada = c.data_instalacao.strftime("%d/%m/%Y")
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(c.id)),
                        ft.DataCell(ft.Text(c.numero_abelhas)),
                        ft.DataCell(ft.Text(c.tipo_abelhas)),
                        ft.DataCell(ft.Text(data_formatada)),
                        ft.DataCell(ft.Text(
                            f"Apiário {apiario.id}" if apiario else ""
                        )),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.BLUE_400,
                                    tooltip="Editar",
                                    on_click=lambda e, c=c: iniciar_edicao(c)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color=ft.colors.RED_400,
                                    tooltip="Deletar",
                                    on_click=lambda e, id=c.id: deletar_colmeia(id)
                                )
                            ])
                        ),
                    ]
                )
            )
        page.update()

    def iniciar_edicao(colmeia):
        nonlocal colmeia_em_edicao, data_selecionada
        colmeia_em_edicao = colmeia
        
        # Preencher campos com dados atuais
        numero_abelhas.value = str(colmeia.numero_abelhas)
        tipo_abelhas.value = colmeia.tipo_abelhas
        data_selecionada = colmeia.data_instalacao
        data_instalacao_display.value = data_selecionada.strftime("%d/%m/%Y")
        apiario_dd.value = str(colmeia.apiario_id)
        
        # Atualizar interface
        btn_salvar.text = "Atualizar"
        btn_cancelar.visible = True
        page.update()

    def cancelar_edicao():
        nonlocal colmeia_em_edicao, data_selecionada
        colmeia_em_edicao = None
        data_selecionada = date.today()
        limpar_campos()
        btn_salvar.text = "Salvar"
        btn_cancelar.visible = False
        page.update()

    def salvar_colmeia(e):
        nonlocal colmeia_em_edicao
        
        if not all([numero_abelhas.value, tipo_abelhas.value, apiario_dd.value]):
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Todos os campos são obrigatórios!"),
                    bgcolor=ft.colors.RED_400
                )
            )
            return
            
        try:
            colmeia = Colmeia(
                id=colmeia_em_edicao.id if colmeia_em_edicao else None,
                numero_abelhas=int(numero_abelhas.value),
                tipo_abelhas=tipo_abelhas.value,
                data_instalacao=data_selecionada,
                apiario_id=int(apiario_dd.value)
            )
            colmeia.salvar()
            limpar_campos()
            atualizar_tabela()
            cancelar_edicao()
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Colmeia salva com sucesso!"),
                    bgcolor=ft.colors.GREEN_400
                )
            )
        except ValueError as error:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Erro de validação: {str(error)}"),
                    bgcolor=ft.colors.RED_400
                )
            )
        except Exception as error:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Erro ao salvar: {str(error)}"),
                    bgcolor=ft.colors.RED_400
                )
            )

    def deletar_colmeia(id):
        try:
            Colmeia.deletar(id)
            atualizar_tabela()
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Colmeia deletada com sucesso!"),
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
        numero_abelhas.value = ""
        tipo_abelhas.value = ""
        data_instalacao_display.value = date.today().strftime("%d/%m/%Y")
        apiario_dd.value = None
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
                                    "Cadastro de Colmeias",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLUE_900
                                ),
                                ft.Column(
                                    [numero_abelhas, tipo_abelhas,
                                     data_container, apiario_dd],
                                    spacing=10
                                ),
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