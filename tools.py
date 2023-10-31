# -*- coding: utf-8 -*-
"""
Este script tiene como objetivo raspar información de dos artículos específicos
sobre equipos de origen ruso y ucraniano. La información se extrae, transforma
y almacena en DataFrames de pandas.

Created on Wed Aug 23 14:24:10 2023
@author: gblancom
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import gc
#import pymysql
from sqlalchemy import create_engine
from urllib.parse import unquote
import re

def extract_lists_from_article(url):
    """
   Extrae listas de artículos a partir de una URL.

   Args:
   - url (str): La URL del artículo.

   Returns:
   - list: Las listas extraídas del artículo.
   - list: Objetos de listas originales para uso adicional.
   """
    # Realizar la solicitud a la URL
    response = requests.get(url)
    response.raise_for_status()  # Si hay un error, lanza una excepción

    # Parsear el contenido con BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar la sección "article"
    article = soup.find('article')
    if not article:
        return []

    # Buscar todas las listas dentro del article
    lists = article.find_all(['ul', 'ol'])

    return lists


def convert_to_int(lst):
    """
    Convierte posibles entradas a enteros, de lo contrario, elimina espacios.

    Args:
    - lst (list): La lista a procesar.

    Returns:
    - list: Lista procesada.
    """

    new_lst = []
    for item in lst:
        try:
            new_item = int(item)
        except ValueError:
            new_item = item.replace(' ', '')
        new_lst.append(new_item)
    return new_lst


def trans_to_df(object):
    """
    Transforma los datos extraídos en un DataFrame.

    Args:
    - object: El objeto que contiene los datos extraídos.

    Returns:
    - DataFrame: Un DataFrame con los datos procesados.
    """
    data = [['weapon', 'origen', 'platform', 'number', 'Status', 'url']]

    total_pistol = ['type']
    strange=0
    for list in object:
        head = list.find_previous('h3').get_text(strip=True).split("(")[0]
        try:
            total_pistol.append(list.find_previous('h3').get_text(strip=True))
        except:
            total_pistol.append('No encontrado')
        for plataforma in list.contents:
            origin = []
            for i, case in enumerate(plataforma.contents):
                if "src" in str(case):
                    try:
                        origin.append(case.attrs['src'])
                    except:
                        try:
                            origin.append(case.find('img').attrs['src'])
                        except:
                            print('Process in controlled exception')
                            problema = case
                            for nested in problema:
                                try:
                                    origin.append(nested.contents[0].attrs['src'])
                                except:
                                    origin.append(nested.contents[0].contents[0].attrs['src'])
                elif 'href' in str(case):
                    try:
                        casos = case.text.replace("(", "").replace(")", "").replace(", and ", "#").replace(",",
                                                                                                           "#").replace(
                            ' and', "#").split("#")
                        end_words = []
                        casos = convert_to_int(casos)
                        for item in reversed(casos):
                            if not isinstance(item, int):
                                end_words.insert(0, item)
                            else:
                                break
                        for j in range(0, len(casos) - len(end_words)):
                            data.append([head, origin, plat, casos[j], end_words, case.attrs['href']])
                    except Exception as d:
                        print(f"Error looking for span: {d}")
                        for span in case:
                            try:
                                a_tag = span.find('a')
                                if (a_tag != -1) & (a_tag is not None):
                                    href = a_tag.attrs['href']
                                    text = a_tag.get_text().replace("(", "").replace(")", "").replace(", and ", "#").replace(",", "#").replace(' and', "#").split("#")
                                    end_words = []
                                    text = convert_to_int(text)
                                    for item in reversed(text):
                                        if not isinstance(item, int):
                                            end_words.insert(0, item)
                                        else:
                                            break
                                    for j in range(0, len(text) - len(end_words)):
                                        data.append([head, origin, plat, text[j], end_words, href])
                                else:
                                    pass
                            except Exception as e:
                                print(f"Error processing span: {e}")
                                pass

                elif len(case) > 3:
                    try:
                        plat = case.text.replace("\xa0", "")
                    except Exception as e:
                        print(f"Error procesing strange things: {e}")
                        print("---> case where it happened --> ", case)
                        if "1 Unknown T-54/55" in case.text:
                            data.append(["Tanks", ['https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/23px-Flag_of_the_Soviet_Union.svg.png'], "1 Unknown T-54/55", 1, ['destroyed'], 'https://twitter.com/CalibreObscura/status/1670510694838546436'])
                        else:
                            strange= strange + 1
                            print("Not managed strange cases = ", strange)
                elif len(case) <= 3:
                    pass
                else:
                    strange = strange + 1
                    print("Not managed strange cases = ", strange)


    return pd.DataFrame(data, columns=data.pop(0)), total_pistol

def extr_country(object):
    pais = []
    for url in object:
        # Decodificamos la URL para convertir los caracteres codificados en caracteres normales

        url = unquote(url)

        # Expresión regular para manejar diferentes casos de URLs
        regex = r"https://upload\.wikimedia\.org/wikipedia/(?:commons|en)/thumb/\w/\w\w/Flag_of_([^/]+).svg/\d+px-Flag_of_[^/]+.svg.png"

        # Intentamos encontrar una coincidencia con la expresión regular
        match = re.search(regex, url)

        # Si hay una coincidencia, retornamos el nombre del país o entidad
        if match:
            # Extraemos el nombre del país y eliminamos cualquier cosa entre paréntesis
            aux = re.sub(r" ?\([^)]+\)", "", match.group(1))
            # Reemplazamos los guiones bajos con espacios
            pais.append(aux.replace('_', ' '))
        else:
            pais.append("Fail To ID Country")
    return pais

def insertar_en_bbdd(df, usuario, contraseña, host, database, table):

    # Crear conexión a la base de datos
    engine = create_engine(f"mysql+pymysql://{usuario}:{contraseña}@{host}/{database}")
    try:
        # Insertar los datos en la tabla 'bajas'
        with engine.connect() as conn:
            df.to_sql(table, con=conn, if_exists='replace', index=False) #if_exists='append'
            # conn.execute('COMMIT;')  # Hacer commit explícitamente
        return "Insertado correctamente"
    except Exception as e:
        return f"Ocurrió un error: {e}"

def clean_url(url):
    # Eliminar espacios al principio y al final
    url = url.strip()

    # Reemplazar tabulaciones con espacios vacíos
    url = url.replace('\t', '')

    return url


def extract_tables_from_url2(url):
    """
    Extrae tablas de una página web y las retorna como una lista de DataFrames de pandas.

    Parámetros:
    url (str): La URL de la página web de donde se extraerán las tablas.

    Retorna:
    list or str: Una lista de DataFrames de pandas, o un mensaje de error si algo sale mal.
    """

    # Define un encabezado de agente de usuario
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://www.google.com/",  # Simula que llegas desde Google
        "Accept-Language": "en-US,en;q=0.9"
    }

    cookies = {
        "session_id": "abc123"  # Reemplaza "abc123" con el valor real de tu cookie
    }

    # Haz una solicitud GET a la URL con el encabezado de agente de usuario y permite redirecciones
    response = requests.get(url, headers=headers, allow_redirects=True)

    # Asegúrate de que la solicitud fue exitosa
    if response.status_code == 200:
        # Si la solicitud fue exitosa, pasa el contenido de la respuesta a pandas.read_html
        tables = pd.read_html(response.text)
        # Retorna las tablas como una lista de DataFrames de pandas
        return tables
    else:
        # Si la solicitud no fue exitosa, retorna un mensaje de error
        return f"Error: {response.status_code}"



def extract_tables_from_url(url, cookies=None, referer=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": referer,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }

    response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=True)

    if response.status_code == 200:
        tables = pd.read_html(response.text)
        return tables
    else:
        return f"Error: {response.status_code}"
