#Diseño/styles 

import pandas as pd
from Funciones.utils import formatear_hora
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

def apply_dataframe_styles(df):
    """Aplica estilos elegantes a los DataFrames."""
    if df.empty:
        return df

    styles = {'Materia': '250px', 'NRC': '100px', 'Día': '180px', 'Horario': '120px', 'Profesor': '300px'}  # Ajustar anchos de columna

    styled_df = df.style \
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'left'), ('background-color', '#f0f0f0'), ('font-weight', 'bold')]},  # Estilo de encabezados
            {'selector': 'td', 'props': [('text-align', 'left'), ('padding', '5px 10px')]},  # Estilo de celdas
            {'selector': 'tr:nth-child(2n)', 'props': [('background-color', '#f8f8f8')]}  # Estilo de filas pares
        ]) \
        .set_properties(**styles)  # Aplicar anchos de columna

    return styled_df

def get_reportlab_styles():
    """Devuelve un diccionario con los estilos de ReportLab."""
    styles = {
        'Title': ParagraphStyle(
            name='Title',
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            spaceAfter=12,
        ),
        'Subtitle': ParagraphStyle(
            name='Subtitle',
            fontName='Helvetica',
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.blue,
            spaceAfter=6,
        ),
        'TableHeader': ParagraphStyle(
            name='TableHeader',
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.black,
        ),
        'Materia': ParagraphStyle(
            name='Materia',
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=9,
            textColor=colors.black,
        ),
        'Aula': ParagraphStyle(
            name='Aula',
            alignment=TA_CENTER,
            fontSize=8,
            leading=9,
            textColor=colors.black,
        ),
        'Profesor': ParagraphStyle(
            name='Profesor',
            alignment=TA_CENTER,
            fontSize=8,
            leading=9,
            textColor=colors.black,
        ),
        'Hora': ParagraphStyle(
            name='Hora',
            alignment=TA_CENTER,
            fontSize=8,
            leading=9,
            textColor=colors.black,
        ),
        'Footer': ParagraphStyle(
            name='Footer',
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey,
            leading=12,
        ),
        'FooterLink': ParagraphStyle(
            name='FooterLink',
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.blue,
            leading=12,
        ),
        'TableCellCenter': ParagraphStyle(  # Estilo para las celdas de la tabla centradas
            name='TableCellCenter',
            fontName='Helvetica',
            fontSize=10,
            leading=12,
            textColor=colors.black,
            alignment=TA_CENTER,
        ),
        'ClashStyle': ParagraphStyle(
            name='ClashStyle',
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=colors.red,
        ),
    }
    return styles

def highlight_cruce(row, clase1, clase2):
    """Resalta la fila si hay un cruce con las clases dadas."""
    hora_row_formateada = formatear_hora(row['Hora'])
    hora_clase1 = f"{clase1.hora_inicio} - {clase1.hora_fin}"
    hora_clase2 = f"{clase2.hora_inicio} - {clase2.hora_fin}"

    if hora_row_formateada and (hora_row_formateada == hora_clase1 or hora_row_formateada == hora_clase2) and row['Días'] == clase1.dia:
        return ['background-color: #e62719'] * len(row)
    return [''] * len(row)

def apply_dataframe_styles_with_cruces(df, cruces):
    """Aplica estilos generales y resalta los conflictos."""
    styled_df = df.style.background_gradient(cmap="Blues")
    if cruces:
        for dia, conflictos in cruces.items():
            for clase1, clase2 in conflictos:
                styled_df = styled_df.apply(highlight_cruce, axis=1, clase1=clase1, clase2=clase2)
    return styled_df