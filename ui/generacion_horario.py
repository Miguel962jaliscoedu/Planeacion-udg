#ui/generacion_horarios

import flet as ft
import pandas as pd
import base64
import io
from Funciones.data_processing import cargar_datos_desde_json, guardar_datos_local
from Funciones.schedule import create_schedule_sheet, create_schedule_pdf
from Diseño.styles import apply_dataframe_styles, get_reportlab_styles

class GeneracionHorario:
    def __init__(self, page):
        self.page = page

    def build(self):
        return ft.ElevatedButton("Generar horario", on_click=self.generar_horario, expand=True)

    def generar_horario(self, e):
        loaded_data = cargar_datos_desde_json()
        if loaded_data:
            expanded_data = pd.DataFrame(loaded_data.get("oferta_academica", []))
            selected_nrcs = loaded_data.get("nrcs_seleccionados", [])
            selected_options = json.loads(self.page.client_storage.get("selected_options"))
            ciclo = selected_options.get("ciclop", {}).get("description")

            if selected_nrcs:
                filtered_data = expanded_data[expanded_data["NRC"].isin(selected_nrcs)]
                if not filtered_data.empty:
                    schedule = create_schedule_sheet(filtered_data)
                    if schedule is not None and not schedule.empty:
                        styled_schedule_df = apply_dataframe_styles(schedule)
                        pdf_buffer = create_schedule_pdf(schedule, ciclo)
                        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')

                        self.page.dialog = ft.AlertDialog(
                            title=ft.Text("Horario generado:"),
                            content=ft.Column([
                                ft.DataTable(
                                    columns=[ft.DataColumn(ft.Text(col)) for col in styled_schedule_df.columns],
                                    rows=[ft.DataRow([ft.DataCell(ft.Text(str(row[col]))) for col in styled_schedule_df.columns]) for _, row in styled_schedule_df.iterrows()]
                                ),
                                ft.Image(src_base64=pdf_base64, width=700, height=1000),
                                ft.ElevatedButton(
                                    text="Descargar Horario",
                                    on_click=lambda e: self.page.launch_url(f"data:application/pdf;base64,{pdf_base64}")
                                )
                            ])
                        )
                        self.page.dialog.open = True
                        self.page.update()

                        # Guardar el horario en el JSON
                        loaded_data["horario_generado"] = schedule.to_dict(orient="records")
                        guardar_datos_local(loaded_data)
                    else:
                        self.page.snack_bar = ft.SnackBar(ft.Text("No se pudo generar el horario. Verifica los datos."))
                        self.page.snack_bar.open = True
                        self.page.update()
                else:
                    self.page.snack_bar = ft.SnackBar(ft.Text("No hay datos para generar el horario con los NRCs seleccionados."))
                    self.page.snack_bar.open = True
                    self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Selecciona al menos un NRC."))
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("No se pudo obtener la información del ciclo. Por favor, realiza una nueva consulta."))
            self.page.snack_bar.open = True
            self.page.update()