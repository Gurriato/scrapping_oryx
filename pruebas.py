def extraer_palabra(url):
    # Lista de expresiones regulares para manejar diferentes casos de URLs
    regexes = [
        r"https://upload\.wikimedia\.org/wikipedia/en/thumb/\w/\w\w/Flag_of_(\w+).svg/\d+px-Flag_of_\w+.svg.png",
        r"https://upload\.wikimedia\.org/wikipedia/commons/thumb/\w/\w\w/Flag_of_(\w+).svg/\d+px-Flag_of_\w+.svg.png",
        r"https://upload\.wikimedia\.org/wikipedia/commons/thumb/\w/\w\w/Flag_of_(\w+)_\(%d{4}-%d{4}\).svg/\d+px-Flag_of_\w+_\(%d{4}-%d{4}\).svg.png",
        r"https://upload\.wikimedia\.org/wikipedia/commons/thumb/\w/\w\w/Flag_of_(\w+)_\(converted\).svg/\d+px-Flag_of_\w+_\(converted\).svg.png",
        r"https://upload\.wikimedia\.org/wikipedia/commons/thumb/\w/\w\w/Flag_of_(\w+)_\(Pantone\).svg/\d+px-Flag_of_\w+_\(Pantone\).svg.png"
    ]
    # Intentamos encontrar una coincidencia con cada expresión regular
    for regex in regexes:
        match = re.search(regex, url)
        if match:
            return match.group(2)  # Retornamos el primer grupo de captura que corresponde a XXX
    # Si no hay coincidencias, retornamos un mensaje indicándolo
    return "No se encontró una coincidencia"


import re


def extraer_pais(url):
    # Expresión regular para manejar diferentes casos de URLs
    regex = r"https://upload\.wikimedia\.org/wikipedia/(?:commons|en)/thumb/\w/\w\w/Flag_of_([a-zA-Z_]+)(?:_\(.+\))?.svg/\d+px-Flag_of_[a-zA-Z_]+(?:_\(.+\))?.svg.png"

    # Intentamos encontrar una coincidencia con la expresión regular
    match = re.search(regex, url)

    # Si hay una coincidencia, retornamos el nombre del país o entidad
    if match:
        return match.group(1)

    # Si no hay coincidencias, retornamos un mensaje indicándolo
    return "No se encontró una coincidencia"


# Puedes probar la función con diferentes URLs para ver cómo funciona
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States_(Pantone).svg/1280px-Flag_of_the_United_States_(Pantone).svg.png"
print(extraer_pais(url))

urls_prueba = [
    ("https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_XXX.svg/23px-Flag_of_Germany.svg.png", "XXX"),
    ("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_XXX.svg/23px-Flag_of_Ukraine.svg.png", "XXX"),
    (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Flag_of_XXX_%281946-1992%29.svg/23px-Flag_of_Yugoslavia_%281946-1992%29.svg.png",
    "XXX"),
    (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Flag_of_XXX_%28converted%29.svg/23px-Flag_of_Australia_%28converted%29.svg.png",
    "XXX"),
    (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_XXX_%28Pantone%29.svg/23px-Flag_of_Canada_%28Pantone%29.svg.png",
    "XXX")
]
# Ejecutamos la función extraer_palabra en cada URL de prueba
for url, esperado in urls_prueba:
    resultado = extraer_pais(url)
    if resultado == esperado:
        print(f"Prueba exitosa para URL: {url}\nResultado esperado: {esperado}\nResultado obtenido: {resultado}\n")
    else:
        print(f"Prueba fallida para URL: {url}\nResultado esperado: {esperado}\nResultado obtenido: {resultado}\n")


def extraer_pais(url):
    # Expresión regular para manejar diferentes casos de URLs
    regex = r"https://upload\.wikimedia\.org/wikipedia/(?:commons|en)/thumb/\w/\w\w/Flag_of_([^/]+).svg/\d+px-Flag_of_[^/]+.svg.png"

    # Intentamos encontrar una coincidencia con la expresión regular
    match = re.search(regex, url)

    # Si hay una coincidencia, retornamos el nombre del país o entidad
    if match:
        # Extraemos el nombre del país y reemplazamos los guiones bajos con espacios
        pais = match.group(1).replace('_', ' ')
        # Retornamos el nombre del país sin modificadores adicionales (como "(Pantone)")
        return re.sub(r" \(.+\)", "", pais)

    # Si no hay coincidencias, retornamos un mensaje indicándolo
    return "No se encontró una coincidencia"

from urllib.parse import unquote
def extraer_pais(url):
    # Decodificamos la URL para convertir los caracteres codificados en caracteres normales
    url = unquote(url)

    # Expresión regular para manejar diferentes casos de URLs
    regex = r"https://upload\.wikimedia\.org/wikipedia/(?:commons|en)/thumb/\w/\w\w/Flag_of_([^/]+).svg/\d+px-Flag_of_[^/]+.svg.png"

    # Intentamos encontrar una coincidencia con la expresión regular
    match = re.search(regex, url)

    # Si hay una coincidencia, retornamos el nombre del país o entidad
    if match:
        # Extraemos el nombre del país y eliminamos cualquier cosa entre paréntesis
        pais = re.sub(r" ?\([^)]+\)", "", match.group(1))
        # Reemplazamos los guiones bajos con espacios
        return pais.replace('_', '')

    # Si no hay coincidencias, retornamos un mensaje indicándolo
    return "No se encontró una coincidencia"


# Función para limpiar los datos
def limpiar_datos(texto):
    # Utilizar una expresión regular para encontrar el primer número y el nombre que sigue
    match = re.search(r'\d+\s+(.*?)\s*:', texto)
    if match:
        numero = int(match.group())
        nombre = match.group(1)
        return numero, nombre
    else:
        return None, None

def limpiar_datos(texto):
    # Utilizar una expresión regular para encontrar el primer número y el nombre que sigue
    match = re.search(r'(\d+)\s+(.*?)\s*:', texto)
    if match:
        numero = int(match.group(1))
        nombre = match.group(2)
        return numero, nombre
    else:
        return None, None

# Aplicar la función de limpieza a la columna
to_file['platform'] = to_file['platform'].apply(limpiar_datos)

# Crear dos nuevas columnas con los resultados
to_file[['total', 'platform']] = pd.DataFrame(to_file['platform'].tolist(), index=to_file.index)

# Eliminar la columna temporal 'Columna'
to_file = to_file.drop('Columna', axis=1)

# Imprimir el DataFrame resultante
print(df)

def extract_lists_and_headings_from_article(url):
    """
    Extrae listas y encabezados de artículos a partir de una URL.

    Args:
    - url (str): La URL del artículo.

    Returns:
    - list: Las listas con encabezados extraídos del artículo.
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

    extracted_lists = []
    for lst in lists:
        # Buscar el encabezado h3 más cercano antes de cada lista
        heading = lst.find_previous('h3')
        heading_text = heading.get_text(strip=True) if heading else 'No heading'

        # Extraer los elementos de la lista
        list_items = [item.get_text(strip=True) for item in lst.find_all('li')]
        extracted_lists.append({
            'heading': heading_text,
            'items': list_items
        })

    return extracted_lists
print(lists[0].find_previous('h3'))

lists[0].find_previous('h3').find('span', class_='mw-headline').get_text()

scraped_object[2].contents[0].contents[1]

data = [['origin', 'type', 'platform', 'number', 'Status', 'url']]
total_pistol = ['type']
for list in lists:
    head = list.find_previous('h3').get_text(strip=True).split("(")[0]
    try:
        total_pistol.append(list.find_previous('h3').get_text(strip=True))
    except:
        total_pistol.append('No encontrado')
    for plataforma in list.contents:
        for i, case in enumerate(plataforma.contents):
            if i == 0:
                try:
                    origin = case.attrs['src']
                except:
                    try:
                        problema = case
                        for nested in problema:
                            try:
                                origin = problema.contents[0].attrs['src']
                            except:
                                problema = problema.contents[0]
                    except:
                        origin = 'others'
            elif i == 1:
                plat = case.text.replace(r"\xa0", "")
            else:
                try:
                    casos = case.text.replace("(", "").replace(")", "").replace(", and ", "#").replace(",",
                                                                                                       "#").replace(
                        ' and', "#").split("#")
                    end_words = []
                    casos = convert_to_int(casos)
                    for item in reversed(casos):
                        if isinstance(item, int):
                            break
                        else:
                            end_words.insert(0, item)
                    for j in range(0, len(casos) - len(end_words)):
                        data.append([head, origin, plat, casos[j], end_words, case.attrs['href']])
                except:
                    print('ERROR en la transformación a DF linea -')
                    pass
    return pd.DataFrame(data, columns = data.pop(0)), total_pistol
def trans_to_df(object):
    """
    Transforma los datos extraídos en un DataFrame.

    Args:
    - object: El objeto que contiene los datos extraídos.

    Returns:
    - DataFrame: Un DataFrame con los datos procesados.
    """
    data = [['origin', 'type', 'platform', 'number', 'Status', 'url']]
    for entry in object:
        type = entry['heading']

        for arma in entry['items']:
            for plataforma in arma.contents:
                for i, case in enumerate(plataforma.contents):
                    if i==0:
                        try:
                           origin = case.attrs['src']
                        except:
                            try:
                                problema = case
                                for nested in problema:
                                    try:
                                        origin = problema.contents[0].attrs['src']
                                    except:
                                        problema = problema.contents[0]
                            except:
                               origin = 'others'
                    elif i==1:
                       plat = case.text.replace(r"\xa0", "")
                    else:
                        try:
                            casos = case.text.replace("(", "").replace(")", "").replace(", and ", "#").replace(",", "#").replace(' and',"#").split("#")
                            end_words = []
                            casos = convert_to_int(casos)
                            for item in reversed(casos):
                                if isinstance(item, int):
                                    break
                                else:
                                    end_words.insert(0, item)
                            for j in range(0,len(casos)-len(end_words)):
                                data.append([origin, type, plat, casos[j], end_words, case.attrs['href']])
                        except:
                            print('ERROR en la transformación a DF linea -')
                            pass
        return pd.DataFrame(data[1:], columns=data[0])


import pandas as pd



def trans_to_df(object):
    """
    Transforma los datos extraídos en un DataFrame.

    Args:
    - object: El objeto que contiene los datos extraídos.

    Returns:
    - DataFrame: Un DataFrame con los datos procesados.
    """
    data = [['origin', 'type', 'platform', 'number', 'Status', 'url']]
    total_pistol = ['type']
    ja,k=0,0

    for list in object:
        ja=ja+1
        k=0
        head = list.find_previous('h3').get_text(strip=True).split("(")[0]
        try:
            total_pistol.append(list.find_previous('h3').get_text(strip=True))
        except:
            total_pistol.append('No encontrado')
        for plataforma in list.contents:
            k=k+1
            Test = False
            for i, case in enumerate(plataforma.contents):
                if "src" in str(case):
                    try:
                        origin = case.attrs['src']
                    except:
                        problema = case
                        for nested in problema:
                            try:
                                origin = problema.contents[0].find['img'].attrs['src']
                            except:
                                origin = problema.contents[0]
                                print(i, ja, k)
                elif 'href' in str(case):
                    try:
                        casos = case.text.replace("(", "").replace(")", "").replace(", and ", "#").replace(",",
                                                                                                           "#").replace(
                            ' and', "#").split("#")
                        end_words = []
                        casos = tools.convert_to_int(casos)
                        for item in reversed(casos):
                            if isinstance(item, int):
                                break
                            else:
                                end_words.insert(0, item)
                        for j in range(0, len(casos) - len(end_words)):
                            data.append([head, origin, plat, casos[j], end_words, case.attrs['href']])
                    except:
                        print('ERROR en la transformación a DF linea -')
                        pass

                elif len(scraped_object[3].contents[9].contents[1])>3:
                    plat = case.text.replace("\xa0", "")


    return pd.DataFrame(data, columns=data.pop(0)), total_pistol

len(scraped_object[3].contents[9].contents[1])>3)
aaa, bbb = trans_to_df(scraped_object)