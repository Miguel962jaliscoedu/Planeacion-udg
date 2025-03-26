import os
import flet as ft
import pandas as pd
import datetime
from ui.footer import Footer
from Diseño import diseño
from Funciones.data_processing import cargar_datos_desde_json
from Funciones.utils import crear_clases_desde_dataframe, detectar_cruces, generar_mensaje_cruces, formatear_hora

VERSION = os.environ.get("VERSION", "Versión de desarrollo")
URL_PAGINA = os.environ.get("URL_PAGINA", "Web de desarrollo")

class SeleccionMaterias:
    def __init__(self, page, mostrar_generacion_horario, mostrar_formulario):
        self.page = page
        self.mostrar_generacion_horario = mostrar_generacion_horario
        self.mostrar_formulario = mostrar_formulario
        self.materias_seleccionadas = []
        self.nrcs_seleccionados = []
        self.materias_filtradas = []

    def mostrar_consulta_inicial(self, page):
        page.clean()
        from ui.consulta_inicial import ConsultaInicial
        consulta_inicial = ConsultaInicial(page, self.mostrar_generacion_horario)
        page.add(consulta_inicial.build())
        page.update()

    def build(self):
        data = cargar_datos_desde_json("datos.json")
        self.materias = data.get("oferta_academica", [])

        self.materias_seleccionadas = []
        self.materias_disponibles = sorted(list(set(materia["Materia"] for materia in self.materias)))

        self.dropdown_materias = ft.Dropdown(
            options=[ft.dropdown.Option(materia) for materia in self.materias_disponibles],
            width=300,
            label="Materia",
            on_change=self.agregar_seleccion,
        )

        self.materias_seleccionadas_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True) #Se agrega el scroll y expand.

        self.filtrar_button = ft.ElevatedButton("Filtrar Materias", on_click=self.filtrar_materias)

        self.tabla_materias, self.tabla_materias_container = diseño.crear_tabla_materias(self.materias)
        self.tabla_nrcs_filtrados, self.tabla_nrcs_filtrados_container = diseño.crear_tabla_nrcs(self.materias)

        self.dropdown_nrcs = ft.Dropdown(
            options=[],
            width=300,
            label="NRC",
            on_change=self.agregar_nrc_seleccionado,
        )

        self.nrcs_seleccionados_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True) #Se agrega el scroll y expand.

        self.filtrar_nrcs_button = ft.ElevatedButton("Filtrar NRCs", on_click=self.filtrar_nrcs)

        self.mensajes_cruces_container = ft.Column()

        footer = Footer(VERSION, URL_PAGINA).build()

        self.generar_horario_button = ft.ElevatedButton("Generar Horario", on_click=self.generar_horario)

        return ft.Column(
            controls=[
                ft.Row(controls=[
                    ft.ElevatedButton("Nueva Consulta", on_click=lambda e: self.mostrar_consulta_inicial(self.page)),
                    ft.ElevatedButton("Formulario de Sugerencias", on_click=lambda e: self.mostrar_formulario(self.page)),
                ]),
                self.dropdown_materias,
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                self.materias_seleccionadas_container,
                                self.filtrar_button,
                                self.tabla_materias_container,
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
                self.dropdown_nrcs,
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                self.nrcs_seleccionados_container,
                                self.filtrar_nrcs_button,
                                self.tabla_nrcs_filtrados_container,
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
                self.mensajes_cruces_container,
                self.generar_horario_button,
                footer,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )

    def agregar_seleccion(self, e):
        materia_seleccionada = self.dropdown_materias.value

        if materia_seleccionada:
            coincidencias_materia = [materia for materia in self.materias if materia["Materia"] == materia_seleccionada]
            self.materias_seleccionadas.extend(coincidencias_materia)

            self.materias_disponibles.remove(materia_seleccionada)
            self.dropdown_materias.options = [ft.dropdown.Option(materia) for materia in self.materias_disponibles]
            self.dropdown_materias.value = None

        self.actualizar_materias_seleccionadas()
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
            self.materias_disponibles.append(seleccion)
            self.materias_disponibles.sort()
            self.dropdown_materias.options = [ft.dropdown.Option(materia) for materia in self.materias_disponibles]

        self.actualizar_materias_seleccionadas()


    def filtrar_materias(self, e):
        print(f"Filtrando materias")  # Depuración
        self.materias_filtradas = self.materias_seleccionadas.copy()
        self.actualizar_tabla(self.materias_filtradas, self.tabla_materias, self.tabla_materias_container)
        self.actualizar_dropdown_nrcs()

    def actualizar_dropdown_nrcs(self):
        nrcs_unicos = list(set(str(materia["NRC"]) for materia in self.materias_filtradas))
        self.dropdown_nrcs.options = [ft.dropdown.Option(nrc) for nrc in nrcs_unicos if nrc not in self.nrcs_seleccionados]
        self.page.update()

    def agregar_nrc_seleccionado(self, e):
        nrc_seleccionado = self.dropdown_nrcs.value
        if nrc_seleccionado and nrc_seleccionado not in self.nrcs_seleccionados:
            self.nrcs_seleccionados.append(nrc_seleccionado)
            self.actualizar_nrcs_seleccionados()
            self.actualizar_dropdown_nrcs()
            self.dropdown_nrcs.value = None

    def actualizar_nrcs_seleccionados(self):
        self.nrcs_seleccionados_container.controls = []
        for nrc in self.nrcs_seleccionados:
            self.nrcs_seleccionados_container.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(nrc),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, n=nrc: self.quitar_nrc_seleccionado(e, n)),
                    ]
                )
            )
        self.page.update()

    def quitar_nrc_seleccionado(self, e, nrc):
        self.nrcs_seleccionados.remove(nrc)
        self.actualizar_nrcs_seleccionados()
        self.actualizar_dropdown_nrcs()
    
    def actualizar_tabla(self, datos, tabla, contenedor, cruces=None):
        print(f"Actualizando tabla")
        tabla.rows = []
        if datos:
            tabla.visible = True
            contenedor.visible = True
            for fila in datos:
                cells = [ft.DataCell(ft.Text(str(fila[col]))) for col in fila]
                if cruces:
                    for dia, clases_cruzadas in cruces.items():
                        for clase1, clase2 in clases_cruzadas:
                            if str(fila["NRC"]) in [str(clase1.nrc), str(clase2.nrc)] and fila["Días"] == dia:
                                hora_formateada = formatear_hora(fila["Hora"])
                                if hora_formateada:
                                    hora_inicio_fila = datetime.datetime.strptime(hora_formateada.split(" - ")[0], "%H:%M").time()
                                    hora_fin_fila = datetime.datetime.strptime(hora_formateada.split(" - ")[1], "%H:%M").time()

                                    if (datetime.datetime.strptime(clase1.hora_inicio, "%H:%M").time() <= hora_inicio_fila <= datetime.datetime.strptime(clase1.hora_fin, "%H:%M").time()) or (datetime.datetime.strptime(clase2.hora_inicio, "%H:%M").time() <= hora_inicio_fila <= datetime.datetime.strptime(clase2.hora_fin, "%H:%M").time()):
                                        for cell in cells:
                                            cell.bgcolor = ft.colors.AMBER_100  # Color de fondo distintivo
                data_row = ft.DataRow(cells=cells)
                tabla.rows.append(data_row)
        else:
            tabla.visible = False
            contenedor.visible = False
        self.page.update()

    def filtrar_nrcs(self, e):
        print(f"Filtrando NRCs")
        materias_filtradas_por_nrc = []

        if self.nrcs_seleccionados:
            for nrc_seleccionado in self.nrcs_seleccionados:
                for materia in self.materias_filtradas:
                    if str(materia["NRC"]) == nrc_seleccionado:
                        materias_filtradas_por_nrc.append(materia)
        else:
            materias_filtradas_por_nrc = self.materias_filtradas.copy()

        # Detección de cruces
        df_materias_filtradas = pd.DataFrame(materias_filtradas_por_nrc)
        clases = crear_clases_desde_dataframe(df_materias_filtradas)
        cruces = detectar_cruces(clases)
        mensajes_cruces = generar_mensaje_cruces(cruces)

        print(f"Cruces detectados: {cruces}")

        self.actualizar_tabla(materias_filtradas_por_nrc, self.tabla_nrcs_filtrados, self.tabla_nrcs_filtrados_container, cruces)

        # Mostrar mensajes de cruces
        self.mensajes_cruces_container.controls = [ft.Text(mensaje) for mensaje in mensajes_cruces]
        self.page.update()

    def generar_horario(self, e): #Se agrega la funcion generar_horario.
        print("Generando horario...")

        # Obtener los datos necesarios (NRCs seleccionados)
        nrcs_seleccionados_data = [
            materia
            for materia in self.materias_filtradas
            if str(materia["NRC"]) in self.nrcs_seleccionados
        ]

        # Pasar los datos a la clase GeneracionHorario
        self.mostrar_generacion_horario(self.page, nrcs_seleccionados_data)
    