#Funciones/form_handler.py

import re
import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup

# URLs
FORM_URL = "https://siiauescolar.siiau.udg.mx/wal/sspseca.forma_consulta"
POST_URL = "https://siiauescolar.siiau.udg.mx/wal/sspseca.consulta_oferta"

# Función para construir el cuerpo de la solicitud POST
def build_post_data(selected_options):
    return {
        "ciclop": selected_options.get("ciclop", {}).get("value", ""),
        "cup": selected_options.get("cup", {}).get("value", ""),
        "majrp": selected_options.get("majrp", {}).get("value", ""),
        "mostrarp": "",
        "crsep": "",
        "materiap": "",
        "horaip": "",
        "horafp": "",
        "edifp": "",
        "aulap": "",
        "ordenp": "0"
    }

def fetch_form_options_with_descriptions(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        important_fields = ["ciclop", "cup"]
        options_data = {}

        for field_name in important_fields:
            select_tag = soup.find("select", {"name": field_name})
            if select_tag:
                options = []
                for option in select_tag.find_all("option"):
                    value = option.get("value", "").strip()
                    text_parts = []
                    for child in option.contents:
                        if isinstance(child, str):
                            text_parts.append(child.strip())
                    full_text = " ".join(text_parts).strip()
                    full_text = re.sub(r'\s+', ' ', full_text).strip()

                    if value:
                        parts = full_text.split("-", 1)
                        if len(parts) == 2:
                            description = parts[1].strip()
                        else:
                            description = full_text.strip()

                        options.append({"value": value, "description": description})
                options_data[field_name] = options
        return options_data

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener las opciones del formulario: {e}")
        return None

def show_abbreviations(cup_value):
    """Muestra la tabla de abreviaturas y devuelve un diccionario de carreras."""
    abrev_url = f"https://siiauescolar.siiau.udg.mx/wal/sspseca.lista_carreras?cup={cup_value}"
    try:
        response = requests.get(abrev_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if table:
            html_string = str(table)
            df = pd.read_html(StringIO(html_string))[0]

            carreras_dict = dict(zip(df['CICLO'], df['DESCRIPCION']))
            return carreras_dict

        else:
            print("Advertencia: No se encontró la tabla de abreviaturas en la página.")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la página de abreviaturas: {e}")
        return {}
    except pd.errors.ParserError as e:
        print(f"Error al parsear la tabla: {e}. Verifica que la tabla tenga un formato correcto.")
        return {}
    except IndexError as e:
        print(f"Error al acceder a la tabla parseada: {e}. Verifica que la tabla tenga un formato correcto.")
        return {}
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return {}