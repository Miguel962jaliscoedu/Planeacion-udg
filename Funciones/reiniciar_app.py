# Funciones/reiniciar_app.py

import flet as ft
import pandas as pd


def reiniciar_aplicacion(page, selected_subjects, selected_nrcs, expanded_data):
    # Eliminar el almacenamiento local
    page.client_storage.clear()  # Borra todo el almacenamiento local

    # Restablecer las variables internas
    selected_subjects.clear()
    selected_nrcs.clear()
    expanded_data = pd.DataFrame()

    # Recargar la página para reiniciar la interfaz
    # Llama al método de construcción para reconstruir la interfaz
    page.add(ft.Text("Reiniciando la aplicación..."))
    page.update()
    # Esperamos un momento y luego actualizamos la interfaz
    page.reload()