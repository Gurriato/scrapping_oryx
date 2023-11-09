# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import unquote
import re
import logging

def extract_lists_from_article(url):
    """
    Fetches an article from the given URL and extracts all unordered (ul) and ordered (ol) lists from it.

    The function sends an HTTP GET request to the specified URL. If the request is successful, it parses
    the response content using BeautifulSoup to find the 'article' tag. It then retrieves all 'ul' and 'ol'
    elements (representing unordered and ordered lists, respectively) within the 'article' element.

    Args:
    - url: str
        The URL of the web page from which the article and its lists are to be extracted.

    Returns:
    - lists: list of bs4.element.Tag
        A list of BeautifulSoup Tag objects, each representing an unordered or ordered list found within
        the 'article' element of the web page. If no 'article' element is found, or if there are no lists
        within the article, an empty list is returned.

    Raises:
    - HTTPError: If the HTTP request to the given URL fails, an HTTPError is raised with details of the failure.

    Example Usage:
    >>> article_lists = extract_lists_from_article('https://example.com/some-article')
    >>> for lst in article_lists:
    ...     print(lst, end='\n\n')

    Note:
    - The function assumes that the relevant content is contained within an 'article' tag in the HTML structure
      of the page at the given URL.
    - The function will return an empty list if the URL does not point to a valid web page, if the web page does
      not contain an 'article' tag, or if there are no lists within the found 'article' tag.
    - The function uses the 'requests' library to fetch the web page content and the 'BeautifulSoup' library for
      parsing HTML, both of which must be installed and available in the Python environment where this function is used.
    """

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    article = soup.find('article')
    if not article:
        return []

    lists = article.find_all(['ul', 'ol'])

    return lists


def convert_to_int(lst):
    """
    Converts elements of a list to integers where possible.

    This function iterates over a list of strings and attempts to convert each element to an integer.
    If an element cannot be converted (e.g., because it contains non-numeric characters), the function
    removes any spaces from the string. The processed elements are then stored in a new list, which is
    returned.

    Args:
    - lst: list of str
        The list of strings to be processed, where some strings are expected to represent integer values.

    Returns:
    - new_lst: list
        A new list with the same elements as the input list, where string representations of integers
        have been converted to actual integers, and strings that could not be converted have had spaces removed.

    Example Usage:
    >>> original_list = ['123', '45', 'six', '7 8', 'nine ten']
    >>> converted_list = convert_to_int(original_list)
    >>> print(converted_list)
    [123, 45, 'six', '78', 'nineten']

    Note:
    - This function does not handle strings that represent negative integers, floating-point numbers, or strings
      containing a mix of digits and letters. Such strings will simply have their spaces removed.
    - The function will raise a ValueError if the list contains elements that are not strings or if the strings
      contain characters that are not digits or spaces.
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
    Transforms a structured list of HTML elements into a pandas DataFrame.

    This function takes a list of HTML elements, each potentially containing nested information about weapons,
    origins, platforms, numbers, statuses, and URLs. It iterates over each element, extracting and organizing the
    relevant text and attributes into a structured list. This list is then converted into a pandas DataFrame.
    Additionally, it collects any encountered weapon type into a separate list.

    Args:
    - object: list of bs4.element.Tag
        A list of BeautifulSoup Tag elements, each representing an HTML container with nested information
        to be extracted.

    Returns:
    - tuple: (pd.DataFrame, list)
        A tuple containing two elements:
        1. A pandas DataFrame with columns corresponding to weapon, origin, platform, number, status, and URL.
        2. A list of weapon types extracted during the processing of the HTML elements.

    Example Usage:
    >>> from bs4 import BeautifulSoup
    >>> html_content = '<html><body>...</body></html>'  # Simplified HTML content
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> html_elements = soup.find_all(...)  # A method call that retrieves relevant HTML elements
    >>> dataframe, weapon_types = trans_to_df(html_elements)
    >>> print(dataframe)
    >>> print(weapon_types)

    Note:
    - This function assumes that the HTML structure is consistent and contains the expected patterns for extracting data.
      If the HTML structure changes, the function may need to be updated.
    - It uses exception handling to manage unexpected content or missing attributes, logging warnings, and errors as appropriate.
    - The function depends on a helper function `convert_to_int` to process numerical data, which is not defined within this function.
    - Logging is used to track and report errors during processing, with specific logging for 'controlled exceptions' and 'strange cases.'
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
                            logging.warning('Process in controlled exception')
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
                        logging.warning(f"Error looking for span: {d}")
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
                                logging.error(f"Error processing span: {e}")
                                pass

                elif len(case) > 3:
                    try:
                        plat = case.text.replace("\xa0", "")
                    except Exception as e:
                        logging.warning(f"Error procesing strange things: {e}")
                        logging.warning("---> case where it happened --> ", case)
                        if "1 Unknown T-54/55" in case.text:
                            data.append(["Tanks", ['https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/23px-Flag_of_the_Soviet_Union.svg.png'], "1 Unknown T-54/55", 1, ['destroyed'], 'https://twitter.com/CalibreObscura/status/1670510694838546436'])
                        else:
                            strange= strange + 1
                            logging.error("Not managed strange cases = ", strange)
                elif len(case) <= 3:
                    pass
                else:
                    strange = strange + 1
                    logging.error("Not managed strange cases = ", strange)


    return pd.DataFrame(data, columns=data.pop(0)), total_pistol

def extr_country(object):
    """
    Extracts country names from a list of Wikimedia Commons URLs pointing to images of flags.

    This function processes a list of URLs, each pointing to a flag image hosted on Wikimedia Commons.
    It uses a regular expression to search each URL for a pattern that matches the name of a country.
    The country name is extracted from the URL, formatted, and added to a list. If the country name
    cannot be identified in a URL, the function adds a placeholder text "Fail To ID Country" to the list.

    Parameters:
    :param object: list of str
        A list containing URLs of flag images from Wikimedia Commons. Each URL is expected to follow
        a specific pattern that includes the country's name as part of the file path.

    Returns:
    :return: list of str
        A list of country names corresponding to the flag images in the URLs provided. If a country
        name cannot be identified from a URL, the list will contain the string "Fail To ID Country" at
        that position.

    Example Usage:
    >>> urls = ["https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Flag_of_Brazil.svg/800px-Flag_of_Brazil.svg.png"]
    >>> extr_country(urls)
    ['Brazil']

    Note:
    The function assumes that the URL pattern will not change. If Wikimedia Commons changes the structure
    of the URLs for flag images, the regular expression pattern may need to be updated.
    """
    country = []
    for url in object:
        url = unquote(url)
        regex = r"https://upload\.wikimedia\.org/wikipedia/(?:commons|en)/thumb/\w/\w\w/Flag_of_([^/]+).svg/\d+px-Flag_of_[^/]+.svg.png"
        match = re.search(regex, url)
        if match:
            aux = re.sub(r" ?\([^)]+\)", "", match.group(1))
            country.append(aux.replace('_', ' '))
        else:
            country.append("Fail To ID Country")
    return country

def insert_in_db(df, user, password, host, database, table):
    """
    Inserts the data from a DataFrame into a specified table in a MySQL database.

    This function establishes a connection to a MySQL database using provided user credentials,
    host address, and database name. It then inserts the data from the DataFrame into the specified
    table. If the table already exists, its contents will be replaced.

    Parameters:
    :param df: DataFrame
        The pandas DataFrame containing the data to be inserted into the MySQL database table.
    :param user: str
        The username for authentication with the MySQL database.
    :param password: str
        The password for authentication with the MySQL database.
    :param host: str
        The host address of the MySQL database server.
    :param database: str
        The name of the database where the table is located.
    :param table: str
        The name of the table where the DataFrame data should be inserted.

    Returns:
    :return: str
        A message indicating the result of the insert operation. "Insert OK" if the operation
        is successful, or an error message that includes the exception raised if the operation
        fails.

    Raises:
    :raises Exception:
        Propagates exceptions that may occur during database connection or data insertion.

    Note:
    The 'if_exists' parameter in the 'to_sql' method is set to 'replace', which will replace
    the existing table with the new data. If you wish to append the data instead, change it to 'append'.
    """
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    try:
        with engine.connect() as conn:
            df.to_sql(table, con=conn, if_exists='replace', index=False) #if_exists='append'
            # conn.execute('COMMIT;')
        return "Insert OK"
    except Exception as e:
        return f"Error: {e}"

def clean_url(url):
    """

    :param url: dirty URL
    :return: cleaned URL
    """
    url = url.strip()
    url = url.replace('\t', '')

    return url


def extract_tables_from_url2(url):
    """
    Extracts tables from a web page and returns them as a list of pandas DataFrames.

    Parameters:
    url (str): The URL of the web page from which the tables will be extracted.

    Returns:
    list or str: A list of pandas DataFrames, or an error message if something goes wrong.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://www.google.com/",  # Simula que llegas desde Google
        "Accept-Language": "en-US,en;q=0.9"
    }

    cookies = {
        "session_id": "abc123"  # Reemplaza "abc123" con el valor real de tu cookie
    }
    response = requests.get(url, headers=headers, allow_redirects=True)

    if response.status_code == 200:
        tables = pd.read_html(response.text)
        return tables
    else:
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
