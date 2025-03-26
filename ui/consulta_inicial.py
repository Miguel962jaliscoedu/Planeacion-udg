import flet as ft
import json
from Funciones.data_processing import fetch_table_data, process_data_from_web
from Funciones.form_handler import fetch_form_options_with_descriptions, show_abbreviations, build_post_data, FORM_URL, POST_URL

class ConsultaInicial:
    def __init__(self, page, main_function):
        self.page = page
        self.main_function = main_function
        self.selected_options = {}
        self.carrera_dropdown = ft.Dropdown(label="Selecciona la carrera:", options=[], width=300)
        self.consultar_button = None

    def build(self):
        self.form_options = fetch_form_options_with_descriptions(FORM_URL)
        if self.form_options:
            self.ciclop_dropdown = ft.Dropdown(
                label="Selecciona una opción para ciclop:",
                options=[ft.dropdown.Option(f"{option['value']} - {option['description']}") for option in self.form_options["ciclop"]],
                width=300,
                on_change=self.actualizar_carreras
            )
            self.cup_dropdown = ft.Dropdown(
                label="Selecciona una opción para cup:",
                options=[ft.dropdown.Option(f"{option['value']} - {option['description']}") for option in self.form_options["cup"]],
                width=300,
                on_change=self.actualizar_carreras
            )
            self.consultar_button = ft.ElevatedButton("Consultar", on_click=self.consultar, expand=True)

            return ft.Column([
                ft.Text("Consulta la Oferta Academica:", size=20, weight="bold"),
                self.ciclop_dropdown,
                self.cup_dropdown,
                self.carrera_dropdown,
                ft.Text("Asegúrate de seleccionar la opción CORRECTA para la carrera, ya que algunos centros universitarios tienen claves de carrera DUPLICADAS.", color="orange"),
                self.consultar_button
            ])
        else:
            return ft.Text("No se pudieron obtener las opciones del formulario", color="red")

    def actualizar_carreras(self, e):
        if self.cup_dropdown.value:
            cup_value = self.cup_dropdown.value.split(" - ")[0]
            carreras_dict = show_abbreviations(cup_value)
            if carreras_dict:
                display_carreras = [f"{abreviatura} - {descripcion}" for abreviatura, descripcion in carreras_dict.items()]
                self.carrera_dropdown.options = [ft.dropdown.Option(option) for option in display_carreras]
                self.page.update()

    def consultar(self, e):
        if not self.ciclop_dropdown.value or not self.cup_dropdown.value or not self.carrera_dropdown.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Debes seleccionar ciclo, centro universitario y carrera."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Consultando la información..."))
            self.page.snack_bar.open = True
            self.page.update()

            self.selected_options = {
                "ciclop": {"value": self.ciclop_dropdown.value.split(" - ")[0], "description": self.ciclop_dropdown.value.split(" - ")[1]},
                "cup": {"value": self.cup_dropdown.value.split(" - ")[0], "description": self.cup_dropdown.value.split(" - ")[1]},
                "majrp": {"value": self.carrera_dropdown.value.split(" - ")[0], "description": self.carrera_dropdown.value.split(" - ")[1]}
            }

            post_data = build_post_data(self.selected_options)
            table_data = fetch_table_data(POST_URL, post_data)

            if table_data is not None and not table_data.empty:
                processed_df = process_data_from_web(table_data)
                oferta_academica = processed_df.to_dict(orient="records")

                data_to_save = {
                    "oferta_academica": oferta_academica,
                    "materias_seleccionadas": [],
                    "nrcs_seleccionados": [],
                    "horario_generado": None,
                    "ciclo": self.selected_options["ciclop"]["description"]
                }
                with open("datos.json", "w") as f:
                    json.dump(data_to_save, f, indent=4)
                self.page.client_storage.set("expanded_data", json.dumps(oferta_academica))

                self.page.clean()
                self.main_function(self.page)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("No se encontraron datos para las opciones seleccionadas."))
                self.page.snack_bar.open = True
                self.page.update()

    def guardar_datos_local(self, data):
        self.page.client_storage.set("datos_guardados", json.dumps(data))