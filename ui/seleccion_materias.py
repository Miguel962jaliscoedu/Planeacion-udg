#ui/seleccion_materias

import flet as ft
import pandas as pd
import json
from Funciones.data_processing import cargar_datos_desde_json, guardar_datos_local
from Funciones.utils import detectar_cruces, crear_clases_desde_dataframe, generar_mensaje_cruces
from Diseño.styles import apply_dataframe_styles, apply_dataframe_styles_with_cruces

class SeleccionMaterias:
    def __init__(self, page):
        self.page = page
        self.selected_subjects = []
        self.selected_nrcs = []
        self.expanded_data = pd.DataFrame()

    def build(self):
        query_state = self.page.client_storage.get("query_state")
        if query_state and query_state["done"]:
            loaded_data = cargar_datos_desde_json()
            if loaded_data:
                self.expanded_data = pd.DataFrame(loaded_data.get("oferta_academica", []))
                self.selected_subjects = loaded_data.get("materias_seleccionadas", [])
                self.selected_nrcs = loaded_data.get("nrcs_seleccionados", [])
                self.schedule = pd.DataFrame(loaded_data.get("horario_generado", [])) if loaded_data.get("horario_generado") else None

            if "Materia" in self.expanded_data.columns and "NRC" in self.expanded_data.columns:
                unique_subjects = self.expanded_data["Materia"].unique().tolist()
                self.subject_dropdown = ft.Dropdown(
                    label="Seleccionar Materias",
                    options=[ft.dropdown.Option(subject) for subject in unique_subjects],
                    on_change=self.update_nrc_dropdown,
                    value=self.selected_subjects[0] if self.selected_subjects else None # muestra el primer valor si existe
                )

                self.nrc_dropdown = ft.Dropdown(
                    label="Selecciona los NRC:",
                    options=[],
                    value=self.selected_nrcs[0] if self.selected_nrcs else None # muestra el primer valor si existe
                )

                self.update_nrc_dropdown() # Cargar los NRC iniciales

                return ft.Column([
                    ft.Text("Selecciona las Materias que deseas incluir en tu horario:", size=20, weight="bold"),
                    self.subject_dropdown,
                    ft.Text("Selecciona las clases que deseas incluir en tu horario:", size=20, weight="bold"),
                    self.nrc_dropdown
                ])
        return ft.Container()

    def update_nrc_dropdown(self, e=None):
        self.selected_subjects = [self.subject_dropdown.value] if self.subject_dropdown.value else [] # convierte el valor a lista
        filtered_by_subject = self.expanded_data.copy()
        if self.selected_subjects:
            filtered_by_subject = self.expanded_data[self.expanded_data["Materia"].isin(self.selected_subjects)]
        unique_nrcs = filtered_by_subject["NRC"].unique().tolist()
        self.nrc_dropdown.options = [ft.dropdown.Option(str(nrc)) for nrc in unique_nrcs]
        self.nrc_dropdown.value = self.selected_nrcs[0] if self.selected_nrcs else None
        self.page.update()

    def did_mount(self):
        query_state = self.page.client_storage.get("query_state")
        if query_state and query_state["done"]:
            loaded_data = cargar_datos_desde_json()
            if loaded_data:
                self.selected_nrcs = loaded_data.get("nrcs_seleccionados", [])
                self.update_nrc_dropdown()