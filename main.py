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
    page.title = "Generador de Horarios"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def mostrar_seleccion_materias(page):
        page.clean()
        page.add(seleccion_materias.build())

    consulta_inicial = ConsultaInicial(page, mostrar_seleccion_materias).build()
    seleccion_materias = SeleccionMaterias(page, mostrar_seleccion_materias)
    generacion_horario = GeneracionHorario(page).build()
    formulario_sugerencias = FormularioSugerencias(page).build()
    footer = Footer(VERSION, URL_PAGINA).build()

    def nueva_consulta(e):
        page.clean()
        page.add(consulta_inicial)

    page.add(
        ft.Text("Planifica tu horario de clases", size=30, weight="bold", text_align=ft.TextAlign.CENTER),
        ft.Divider(),
        consulta_inicial,
        formulario_sugerencias,
        footer
    )

ft.app(target=main)