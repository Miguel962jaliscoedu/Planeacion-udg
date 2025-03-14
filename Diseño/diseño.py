#Diseño/diseño.py

import flet as ft

def crear_tabla_materias(materias):
    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in materias[0].keys()],
        rows=[],
        width=800,
        height=400,
        visible=False,
        border=ft.border.all(1, ft.colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.BLACK),
    )

    contenedor = ft.Container(
        content=ft.ListView(
            controls=[tabla],
            expand=True,
        ),
        expand=True,
        height=300,
        visible=False,
    )

    return tabla, contenedor

def crear_tabla_nrcs(materias):
    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(col)) for col in materias[0].keys()],
        rows=[],
        width=800,
        height=400,
        visible=False,
        border=ft.border.all(1, ft.colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.BLACK),
    )

    contenedor = ft.Container(
        content=ft.ListView(
            controls=[tabla],
            expand=True,
        ),
        expand=True,
        height=300,
        visible=False,
    )

    return tabla, contenedor