# -*- coding: utf-8 -*-


import pandas as pd
import gc
import tools
import json
import datetime as dt
import hashlib
import logging
import datetime as dt


def generate_short_hash(row):
    hash_input = '_'.join([str(row['weapon']), str(row['platform']), str(row['number']), str(row['url'])])
    return "_"+str(hashlib.sha256(hash_input.encode()).hexdigest()[:20])


def scrappingOryx(urlLU, owner):
    """
    Scrapes equipment loss data from specified URLs and stores the data in a database and CSV files.

    This function performs web scraping on two specific URLs, each corresponding to equipment losses for Russia
    and Ukraine. It processes the scraped HTML to extract meaningful data and organizes it into pandas DataFrames.
    The data is then cleaned, transformed, and inserted into a specified database. Additionally, the raw and
    aggregated data are saved as CSV files.

    The function relies on a configuration file named 'config.json' for database connection parameters and uses
    custom tools from a module named 'tools' to perform various steps of the scraping and data transformation process.

    Parameters:
        - urlRU: string
            url pointing to the Russian blog entry
        - urlUA: string
            url pointing to the Ucranian blog entry
    Returns:
    - tuple: (pd.DataFrame, pd.Series, pd.Series)
        A tuple containing three elements:
        1. A pandas DataFrame with the combined scraped data for both Russia and Ukraine.
        2. A pandas Series containing the aggregated total equipment losses for Ukraine.
        3. A pandas Series containing the aggregated total equipment losses for Russia.

    Raises:
    - HTTPError: If an HTTP request to one of the specified URLs fails.
    - ValueError: If there are issues with data type conversions or if data extraction regex patterns do not match.

    Example Usage:
    >>> scraped_data, total_ua, total_ru = scrappingOryx()
    >>> print(scraped_data)
    >>> print(total_ua)
    >>> print(total_ru)

    Note:
    - The 'config.json' file must be present in the same directory as this function and contain the necessary database
      credentials and parameters.
    - The function assumes the structure of the web pages at the given URLs remains consistent and that the data follows
      the patterns expected by the regex expressions used for extraction.
    - The function uses several utility functions (such as 'extract_lists_from_article', 'trans_to_df', 'extr_country',
      'clean_url', and 'insert_in_db') which should be defined in the 'tools' module.
    - The function uses the logging module to log information and errors during execution.
    - The 'gc.collect()' call is used to force garbage collection and free memory.
    """

    column_order = ['owner', 'origen', 'weapon', 'platform', 'total', 'number', 'Status', 'url']

    # Russia scrap
    scraped_object = tools.extract_lists_from_article(urlLU)
    LU, total_LU = tools.trans_to_df(scraped_object)
    LU['origen'] = LU['origen'].apply(tools.extr_country)
    LU[['total', 'platform']] = LU['platform'].str.extract(r'(\d+)\s?([^:]+)', expand=True)
    LU['owner'] = owner
    LU = LU[column_order].reset_index(drop=True)
    LU['url'] = LU['url'].apply(tools.clean_url)

    # concat and final cleaning
    # to_file = pd.concat([LU, UA])
    # to_file = to_file.reset_index(drop=True)
    LU['url'] = LU['url'].apply(tools.clean_url)

    # Memory
    scraped_object = None
    gc.collect()

    LU['primary_key'] = LU.apply(generate_short_hash, axis=1)

    # LU.to_csv('./Data/scrap_raw/scrap_raw_' + str(now.date()) + '.csv')

    # Transforming Totals
    regex = r"^(.+?)\s*\((\d+), of which( destroyed: (\d+))?(, damaged: (\d+))?(, abandoned: (\d+))?(, captured: (\d+))?\)$"
    total_LU = pd.Series(total_LU)
    total_LU = total_LU.str.extract(regex)
    total_LU.columns = ['Type', 'Total', 'd1', 'Destroyed', 'd2', 'Damaged', 'd3', 'Abandoned', 'd4', 'Captured']
    total_LU.drop(['d1', 'd2', 'd3', 'd4'], axis=1, inplace=True)
    total_LU = total_LU[1:]
    total_LU.fillna(0, inplace=True)
    total_LU[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']] = total_LU[['Total', 'Destroyed', 'Damaged', 'Abandoned', 'Captured']].astype(int)

    return LU, total_LU


def dataReport():
    """
    auxiliary for creating pandas profiling report
    :return: 
    """
    
    from ydata_profiling import ProfileReport
    report = pd.read_csv(r'.\Data\scrap_raw.csv')
    profile = ProfileReport(report, title="Oryx Data Report")
    profile.to_file(r'.\informe.html')


def compare_dataframes(df_a, df_b, df_excepciones):
    """
    Compares two dataframes to identify the differences, excluding any exceptions provided.

    This function takes two dataframes that are expected to have a 'primary_key' column and compares them to find
    records that are unique to each dataframe. It also accepts a third dataframe containing exceptions which lists
    primary keys that should be excluded from the comparison in each dataframe.

    Parameters:
    - df_a: pd.DataFrame
        The first dataframe to be compared, considered as the base dataframe.
    - df_b: pd.DataFrame
        The second dataframe to be compared, considered as the new dataframe.
    - df_excepciones: pd.DataFrame
        A dataframe containing two columns 'primary_key_base' and 'primary_key_new' which list the primary keys
        that should be excluded from the comparison in df_a and df_b respectively.

    Returns:
    - tuple of pd.DataFrame
        A tuple containing two dataframes:
        1. df_a_difference: Dataframe containing the records that are unique to df_a after filtering out exceptions.
        2. df_b_difference: Dataframe containing the records that are unique to df_b after filtering out exceptions.

    Example Usage:
    >>> df_base = pd.DataFrame({'primary_key': [1, 2, 3], 'data': ['a', 'b', 'c']})
    >>> df_new = pd.DataFrame({'primary_key': [2, 3, 4], 'data': ['b', 'c', 'd']})
    >>> df_exceptions = pd.DataFrame({'primary_key_base': [3], 'primary_key_new': [4]})
    >>> df_base_diff, df_new_diff = compare_dataframes(df_base, df_new, df_exceptions)
    >>> print(df_base_diff)
    >>> print(df_new_diff)

    Note:
    - The function assumes that 'primary_key' columns in df_a and df_b are unique identifiers for their respective records.
    - The function does not handle cases where the 'primary_key' columns have duplicates within the same dataframe.
    - The exceptions are applied to each dataframe separately, based on the relevant column in df_excepciones.
    """
    exceptions_a = set(df_excepciones['primary_key_base'])
    exceptions_b = set(df_excepciones['primary_key_new'])
    df_a_filt = df_a[~df_a['primary_key'].isin(exceptions_a)]
    df_b_filt = df_b[~df_b['primary_key'].isin(exceptions_b)]
    df_b_keys = set(df_b_filt['primary_key'])
    df_a_difference = df_a_filt[~df_a_filt['primary_key'].isin(df_b_keys)]
    df_a_keys = set(df_a_filt['primary_key'])
    df_b_difference = df_b_filt[~df_b_filt['primary_key'].isin(df_a_keys)]
    return df_a_difference, df_b_difference


def pushToDB(data, table):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    try:
        data['Status'] = data['Status'].astype(str)
        data['origen'] = data['origen'].astype(str)
    except:
        pass
    outcome = tools.insert_in_db(data, config['usuario'], config['pass'], config['host'], config['database'], table=table)
    logging.info('insert in table ' + table + outcome)


if __name__ == '__main__':
    logging.basicConfig(filename='./oryxScrapper.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    now = dt.datetime.now()
    urlRU = 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html'
    urlUA = 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html'
    RU, total_RU = scrappingOryx(urlRU, 'RU')
    total_RU.to_csv('./Data/scrap_Total_RU' + str(now.date()) + '.csv')
    UA, total_UA = scrappingOryx(urlUA, 'UA')
    total_UA.to_csv('./Data/scrap_Total_UA' + str(now.date()) + '.csv')
    all = pd.concat([RU, UA]).reset_index(drop=True)
    all.to_csv('./Data/scrap_raw/scrap_raw_' + str(now.date()) + '.csv')

    exceptions = pd.read_csv('./Data/exceptions.csv', sep=';')
    base = pd.read_csv('./Data/base.csv', sep=';', dtype={'total': int, 'number': int, 'primary_key': str})
    #base['primary_key'] = base.apply(generate_short_hash, axis=1)
    df_results_base, df_results_new = compare_dataframes(base, all, exceptions)  #nuevas lineas a incluir
    now = dt.datetime.now()
    if df_results_base.shape[0] != 0:
        df_results_base.to_csv('./Data/diff/excep_base_' + str(now.date()) + '.csv')
    df_results_new.to_csv('./Data/diff/excep_new_' + str(now.date()) + '.csv')

    df_results_new['Date'] = dt.datetime.now().strftime("%d/%m/%Y")
    logging.info('New rows added: ' + str(df_results_new.shape[0]))
    base = pd.concat([base, df_results_new])
    # Use this line instead of next if you want to see the real count of Oryx
    #base['total_real'] = base.groupby(['owner', 'weapon', 'platform'])['owner'].transform('size')
    base['total'] = base.groupby(['owner', 'weapon', 'platform'])['owner'].transform('size')
    pushToDB(base, 'bajas')
    pushToDB(total_RU, 'total_RU')
    pushToDB(total_UA, 'total_UA')
    base['total'] = pd.to_numeric(base['total'], errors='coerce').fillna(0).astype(int)
    base.to_csv('./Data/base.csv', sep=';', index=False)


# Data
# https://www.ifw-kiel.de/publications/ukraine-support-tracker-data-20758/
# https://www.oryxspioenkop.com/2023/04/sudan-on-fire-documenting-equipment.html
# https://www.oryxspioenkop.com/2023/04/list-listing-oryx-list-of-lists.html

