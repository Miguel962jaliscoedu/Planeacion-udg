#ui/generacion_horarios

import flet as ft
import pandas as pd
import base64
import io
import json
from Funciones.schedule import create_schedule_sheet, create_schedule_pdf
from Diseño.styles import apply_dataframe_styles, get_reportlab_styles

class GeneracionHorario:
    def __init__(self, page, nrcs_seleccionados_data, mostrar_consulta_inicial, mostrar_formulario):
        self.page = page
        self.nrcs_seleccionados_data = nrcs_seleccionados_data
        self.mostrar_consulta_inicial = mostrar_consulta_inicial
        self.mostrar_formulario = mostrar_formulario

    def mostrar_consulta_inicial(self, page):
        page.clean()
        from ui.consulta_inicial import ConsultaInicial
        consulta_inicial = ConsultaInicial(page, self.mostrar_generacion_horario)
        page.add(consulta_inicial.build())
        page.update()

    def build(self):
        # Ejecutar la lógica de generación del horario aquí
        if self.nrcs_seleccionados_data:
            expanded_data = pd.DataFrame(self.nrcs_seleccionados_data)
            selected_options_str = self.page.client_storage.get("selected_options")
            if selected_options_str:
                selected_options = json.loads(selected_options_str)
                ciclo = selected_options.get("ciclop", {}).get("description")

                if not expanded_data.empty:
                    schedule = create_schedule_sheet(expanded_data)
                    if schedule is not None and not schedule.empty:
                        styled_schedule_df = apply_dataframe_styles(schedule)
                        pdf_buffer = create_schedule_pdf(schedule, ciclo)
                        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')

                        # Mostrar el horario generado
                        return ft.Column(
                            controls=[
                                ft.Row(controls=[
                                    ft.ElevatedButton("Nueva Consulta", on_click=lambda e: self.mostrar_consulta_inicial(self.page)),
                                    ft.ElevatedButton("Formulario de Sugerencias", on_click=lambda e: self.mostrar_formulario(self.page)),
                                ]),
                                ft.DataTable(
                                    columns=[ft.DataColumn(ft.Text(col)) for col in styled_schedule_df.columns],
                                    rows=[ft.DataRow([ft.DataCell(ft.Text(str(row[col]))) for col in styled_schedule_df.columns]) for _, row in styled_schedule_df.iterrows()]
                                ),
                                ft.Image(src_base64=pdf_base64, width=700, height=1000),
                                ft.ElevatedButton(
                                    text="Descargar Horario",
                                    on_click=lambda e: self.page.launch_url(f"data:application/pdf;base64,{pdf_base64}")
                                )
                            ]
                        )
                    else:
                        return ft.Column(
                            controls=[
                                ft.Row(controls=[
                                    ft.ElevatedButton("Nueva Consulta", on_click=lambda e: self.mostrar_consulta_inicial(self.page)),
                                    ft.ElevatedButton("Formulario de Sugerencias", on_click=lambda e: self.mostrar_formulario(self.page)),
                                ]),
                                ft.Text("No se pudo generar el horario. Verifica los datos.")
                            ]
                        )
                else:
                    return ft.Column(
                        controls=[
                            ft.Row(controls=[
                                ft.ElevatedButton("Nueva Consulta", on_click=lambda e: self.mostrar_consulta_inicial(self.page)),
                                ft.ElevatedButton("Formulario de Sugerencias", on_click=lambda e: self.mostrar_formulario(self.page)),
                            ]),
                            ft.Text("No hay datos para generar el horario con los NRCs seleccionados.")
                        ]
                    )
            else:
                return ft.Column(
                    controls=[
                        ft.Row(controls=[
                            ft.ElevatedButton("Nueva Consulta", on_click=lambda e: self.mostrar_consulta_inicial(self.page)),
                            ft.ElevatedButton("Formulario de Sugerencias", on_click=lambda e: self.mostrar_formulario(self.page)),
                        ]),
                        ft.Text("No se pudo obtener la información del ciclo. Por favor, realiza una nueva consulta.")
                    ]
                )
        else:
            return ft.Column(
                controls=[
                    ft.Row(controls=[
                        ft.ElevatedButton("Nueva Consulta", on_click=lambda e: self.mostrar_consulta_inicial(self.page)),
                        ft.ElevatedButton("Formulario de Sugerencias", on_click=lambda e: self.mostrar_formulario(self.page)),
                    ]),
                    ft.Text("Selecciona al menos un NRC.")
                ]
            )