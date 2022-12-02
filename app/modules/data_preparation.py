import os
import pandas as pd

from modules.utils.util_log import info, error
# from utils.util_log import info, error

def get_filenames_and_required_columns(data_path='data/input/'):
    """This function will return full file paths and column names to work with
    Data source is kaggle dataset
    https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
    
    We need 4 tables here
    1) data/input/olist_orders_dataset.csv - here we have order_id, order_status and order_purchase_timestamp
    2) data/input/olist_order_items_dataset.csv - here we have order_id, product_id, seller_id and price per item
    3) data/input/olist_products_dataset.csv - here we have product_id and product_category_name
    4) data/input/olist_sellers_dataset.csv - here we have seller_id, seller_city and seller_state

    Args:
        data_path (str, required): path to the folder with raw data downloaded from kaggle. Defaults to '../data/input/'.

    Returns:
        filenames list: list of filemanes of tables to work with
        required_columns list: list of columnnames to work with 
    """
    orders_file_path = data_path + 'olist_orders_dataset.csv'
    order_items_file_path = data_path + 'olist_order_items_dataset.csv'
    products_file_path = data_path + 'olist_products_dataset.csv'
    sellers_file_path = data_path + 'olist_sellers_dataset.csv'

    orders_col_list = ['order_id', 'order_status', 'order_purchase_timestamp']
    order_items_col_list = ['order_id', 'product_id', 'seller_id', 'price']
    products_col_list = ['product_id', 'product_category_name']
    sellers_col_list = ['seller_id', 'seller_city', 'seller_state']
    
    filenames = [orders_file_path, order_items_file_path, products_file_path, sellers_file_path]
    required_columns = [orders_col_list, order_items_col_list, products_col_list, sellers_col_list]
    
    return zip(filenames, required_columns)


def import_and_check_dataframe(filepath: str, col_list: list, log=None):
    """this small function imports dataframe with only required columns and checks imported dataframe's shape

    Args:
        filepath (str): filepath to the file
        col_list (list): list of required columns

    Returns:
        df (pandas.DataFrame): imported table
    """
    filename = os.path.basename(filepath)
    df = pd.read_csv(filepath, usecols=col_list)

    if log:
        if ~df.empty:
            log(filename + ' imported sucsessfully. Shape is ' + str(df.shape))
        else:
            log('Empty dataframe! Check file')

    return df


def get_all_dataframes(log=None):
    """this function imports all tables into one list of dataframes

    Args:
        log (one of a types from app/modules/utils/util_log.py, optional): can be info, debug, warn, error or None. Defaults to None.
    """

    all_dataframes = []
    for i in get_filenames_and_required_columns():
        all_dataframes.append(import_and_check_dataframe(i[0], i[1], log=log))
        
    all_dataframes = transform_data(all_dataframes, log=log)
        
    return all_dataframes


def transform_dtypes(all_dataframes, log=None):
    """this function transforms column's dtypes. Right now it has only one transformation but in real project there could be more

    Args:
        all_dataframes (list with pd.DataFrames): tables that we want to work with
        log (one of a types from app/modules/utils/util_log.py, optional): can be info, debug, warn, error or None. Defaults to None.

    Returns:
        all_dataframes (list with pd.DataFrames): same tables but with correct dtypes
    """
    try:
        all_dataframes[0]['order_purchase_timestamp'] = pd.to_datetime(all_dataframes[0]['order_purchase_timestamp'])
        log('dtypes transformation is complete')
    except:
        error('something wrong with the "olist_orders_dataset.csv" file')

    return all_dataframes


def fill_missing_values(all_dataframes, log=None):
    try:
        all_dataframes[2]['product_category_name'] = all_dataframes[2]['product_category_name'].fillna('unknown_category')
        log('filling missing values procedure is complete')
    except:
        error('something wrong with the "olist_orders_dataset.csv" file')

    return all_dataframes


def transform_data(all_dataframes, log=None):
    all_dataframes = transform_dtypes(all_dataframes, log=log)
    all_dataframes = fill_missing_values(all_dataframes, log=log)
    return all_dataframes


def create_one_big_table(all_dataframes, log=None):
    try:
        df_orders_plus = pd.merge(all_dataframes[0], all_dataframes[1], on='order_id')
        df_orders_plus = df_orders_plus.merge(all_dataframes[2], on='product_id')
        df_orders_plus = df_orders_plus.merge(all_dataframes[3], on='seller_id')
        log('tables merged sucsessfully')
        return df_orders_plus
    except:
        error('could not merge tables, check files')
        return None
    

def get_data(log=None):
    all_dataframes = get_all_dataframes(log=log)
    df_orders_plus = create_one_big_table(all_dataframes, log=log)
    return df_orders_plus


if __name__ == "__main__":
    log = info
    df_orders_plus = get_data(log=log)
    print(df_orders_plus)
