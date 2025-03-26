#ui/formulario_sugerencias.py

import flet as ft

class FormularioSugerencias:
    def __init__(self, page, mostrar_consulta_inicial):
        self.page = page
        self.form_url = "https://docs.google.com/forms/d/e/1FAIpQLScc5fCcNo9ZocfuqDhJD5QOdbdTNP_RnUhTYAzkEIEFHIB2rA/viewform?embedded=true"
        self.mostrar_consulta_inicial = mostrar_consulta_inicial

    def mostrar_consulta_inicial(self, page):
        page.clean()
        from ui.consulta_inicial import ConsultaInicial # Importa ConsultaInicial dentro de la funcion.
        consulta_inicial = ConsultaInicial(page, self.mostrar_generacion_horario)
        page.add(consulta_inicial.build())
        page.update()

    def build(self):
        return ft.ExpansionTile(
            title=ft.Text(" Hacer una sugerencia o queja"),
            controls=[
                ft.WebView(self.form_url, height=600),
                ft.ElevatedButton("Nueva Consulta", on_click=lambda e: self.mostrar_consulta_inicial(self.page)),
            ]
        )