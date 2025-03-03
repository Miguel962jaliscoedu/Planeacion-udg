#ui/formulario_sugerencias.py

import flet as ft

class FormularioSugerencias:
    def __init__(self, page):
        self.page = page
        self.form_url = "https://docs.google.com/forms/d/e/1FAIpQLScc5fCcNo9ZocfuqDhJD5QOdbdTNP_RnUhTYAzkEIEFHIB2rA/viewform?embedded=true"

    def build(self):
        return ft.ExpansionTile(
            title=ft.Text(" Hacer una sugerencia o queja"),
            controls=[
                ft.WebView(self.form_url, height=600)
            ]
        )