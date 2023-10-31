import pandas as pd
from tools import convert_to_int

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
                                    print(i, ja, k)
                elif 'href' in str(case):
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

                elif len(case)>3:
                    plat = case.text.replace("\xa0", "")


    return pd.DataFrame(data, columns=data.pop(0)), total_pistol

#len(scraped_object[3].contents[9].contents[1])>3)
#aaa, bbb = trans_to_df(scraped_object)