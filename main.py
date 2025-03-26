import flet as ft
from ui.consulta_inicial import ConsultaInicial
from ui.seleccion_materias import SeleccionMaterias
from ui.generacion_horario import GeneracionHorario
from ui.footer import Footer
from ui.formulario_sugerencias import FormularioSugerencias
import os

VERSION = os.environ.get("VERSION", "Versión de desarrollo")
URL_PAGINA = os.environ.get("URL_PAGINA", "Web de desarrollo")

def main(page: ft.Page):
    page.title = "Planeacion de Horario"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def mostrar_seleccion_materias(page):
        page.clean()
        seleccion_materias = SeleccionMaterias(page, mostrar_generacion_horario, mostrar_formulario) # Se agrega mostrar_formulario
        page.add(seleccion_materias.build())

    def mostrar_generacion_horario(page, nrcs_seleccionados_data):
        page.clean()
        generacion_horario = GeneracionHorario(page, nrcs_seleccionados_data, mostrar_consulta_inicial, mostrar_formulario) # Se agrega mostrar_formulario
        page.add(generacion_horario.build())

    def mostrar_consulta_inicial(page):
        page.clean()
        page.add(consulta_inicial.build())

    def mostrar_formulario(page):
        page.clean()
        formulario_sugerencias = FormularioSugerencias(page, mostrar_consulta_inicial).build() # Se agrega mostrar_consulta_inicial
        page.add(formulario_sugerencias)

    consulta_inicial = ConsultaInicial(page, mostrar_seleccion_materias)
    footer = Footer(VERSION, URL_PAGINA).build()

    page.add(
        ft.Text("Planifica tu horario de clases", size=30, weight="bold", text_align=ft.TextAlign.CENTER),
        ft.Divider(),
        consulta_inicial.build(),
        ft.ElevatedButton("Formulario de Sugerencias", on_click=lambda e: mostrar_formulario(page)), # Boton para ir al formulario
        footer
    )

ft.app(target=main)