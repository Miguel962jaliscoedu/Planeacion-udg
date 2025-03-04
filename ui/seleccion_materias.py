import os
import flet as ft
import json
import pandas as pd
from ui.footer import Footer
from Funciones.data_processing import cargar_datos_desde_json
from Funciones.utils import crear_clases_desde_dataframe, detectar_cruces, generar_mensaje_cruces

VERSION = os.environ.get("VERSION", "Versión de desarrollo")
URL_PAGINA = os.environ.get("URL_PAGINA", "Web de desarrollo")

class SeleccionMaterias:
    def __init__(self, page, mostrar_seleccion_materias_callback):
        self.page = page
        self.mostrar_seleccion_materias_callback = mostrar_seleccion_materias_callback
        self.materias_seleccionadas = []
        self.nrcs_seleccionados = []
        self.materias_filtradas = []

    def build(self):
        data = cargar_datos_desde_json("consulta_data.json")
        self.materias = data.get("oferta_academica", [])

        # Dropdown para materias
        materias_unicas = list(set(materia["Materia"] for materia in self.materias))
        self.dropdown_materias = ft.Dropdown(
            options=[ft.dropdown.Option(materia) for materia in materias_unicas],
            width=300,
            label="Materia"
        )

        self.materias_seleccionadas_container = ft.Column()

        self.agregar_button = ft.ElevatedButton("Agregar", on_click=self.agregar_seleccion)
        self.filtrar_button = ft.ElevatedButton("Filtrar Materias", on_click=self.filtrar_materias)

        self.tabla_materias = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in self.materias[0].keys()],
            rows=[],
            width=800,
            height=400,
            visible=False,
        )

        # Dropdown para NRCs (se crea aquí pero se actualiza después)
        self.dropdown_nrcs = ft.Dropdown(
            options=[],
            width=300,
            label="NRC"
        )

        self.filtrar_nrcs_button = ft.ElevatedButton("Filtrar NRCs", on_click=self.filtrar_nrcs)

        # Nueva tabla para NRCs filtrados
        self.tabla_nrcs_filtrados = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col)) for col in self.materias[0].keys()],
            rows=[],
            width=800,
            height=400,
            visible=False,
        )

        footer = Footer(VERSION, URL_PAGINA).build()

        return ft.Column(
            controls=[
                self.dropdown_materias,
                self.agregar_button,
                self.materias_seleccionadas_container,
                self.filtrar_button,
                self.tabla_materias,
                self.dropdown_nrcs,
                self.filtrar_nrcs_button,
                self.tabla_nrcs_filtrados,
                footer,
            ]
        )

    def agregar_seleccion(self, e):
        materia_seleccionada = self.dropdown_materias.value

        if materia_seleccionada:
            coincidencias_materia = [materia for materia in self.materias if materia["Materia"] == materia_seleccionada]
            self.materias_seleccionadas.extend(coincidencias_materia)

        self.actualizar_materias_seleccionadas()
        self.dropdown_materias.value = None
        self.page.update()

    def actualizar_materias_seleccionadas(self):
        nombres_unicos = list(set(materia["Materia"] for materia in self.materias_seleccionadas))

        self.materias_seleccionadas_container.controls = []

        if nombres_unicos:
            self.materias_seleccionadas_container.controls.append(ft.Text("Materias:"))
            for materia in nombres_unicos:
                self.materias_seleccionadas_container.controls.append(
                    ft.Row(
                        controls=[
                            ft.Text(materia),
                            ft.IconButton(ft.icons.DELETE, on_click=lambda e, m=materia: self.quitar_seleccion(e, m, "materia")),
                        ]
                    )
                )

        self.page.update()

    def quitar_seleccion(self, e, seleccion, tipo):
        if tipo == "materia":
            self.materias_seleccionadas = [m for m in self.materias_seleccionadas if m["Materia"] != seleccion]
        self.actualizar_materias_seleccionadas()

    def filtrar_materias(self, e):
        self.materias_filtradas = self.materias_seleccionadas.copy()
        self.actualizar_tabla(self.materias_filtradas, self.tabla_materias)
        self.actualizar_dropdown_nrcs()

    def filtrar_nrcs(self, e):
        materias_filtradas = self.materias_filtradas.copy()

        # Filtrar por NRC solo las materias filtradas
        if self.nrcs_seleccionados:
            materias_filtradas = [
                materia
                for materia in materias_filtradas
                if any(str(nrc["NRC"]) == str(materia["NRC"]) for nrc in self.nrcs_seleccionados)
            ]

        self.actualizar_tabla(materias_filtradas, self.tabla_nrcs_filtrados)

        # Detectar cruces de horarios
        df_materias_filtradas = pd.DataFrame(materias_filtradas)
        clases = crear_clases_desde_dataframe(df_materias_filtradas)
        cruces = detectar_cruces(clases)
        mensajes_cruces = generar_mensaje_cruces(cruces)

        if mensajes_cruces:
            mensaje = "Se detectaron cruces de horarios:\n" + "\n".join(mensajes_cruces)
            self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
            self.page.snack_bar.open = True
            self.page.update()

    def actualizar_tabla(self, materias_filtradas, tabla):
        rows = []
        for materia in materias_filtradas:
            rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(materia[col]))) for col in materia.keys()]
                )
            )

        tabla.rows = rows
        tabla.visible = True
        self.page.update()

    def actualizar_dropdown_nrcs(self):
        nrcs_unicos = list(set(str(materia["NRC"]) for materia in self.materias_filtradas))
        self.dropdown_nrcs.options = [ft.dropdown.Option(nrc) for nrc in nrcs_unicos]
        self.page.update()