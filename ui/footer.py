#ui/footer.py

import flet as ft

class Footer:
    def __init__(self, version, url_pagina):
        self.version = version
        self.url_pagina = url_pagina

    def build(self):
        return ft.Container(
            content=ft.Text(
                f"Desarrollado con la ayuda de IA (ChatGPT y Gemini) | Versión: {self.version} | {self.url_pagina}",
                text_align=ft.TextAlign.CENTER
            ),
            padding=10,
            alignment=ft.alignment.bottom_center
        )