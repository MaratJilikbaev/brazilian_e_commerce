import os
import pandas as pd

from modules.utils.util_log import info
# from utils.util_log import info

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


def get_data(log=None):
    def import_and_check_dataframe(filepath: str, col_list):
        filename = os.path.basename(filepath)
        df = pd.read_csv(filepath, usecols=col_list)

        if log:
            if ~df.empty:
                log(filename + ' imported sucsessfully! Shape is ' + str(df.shape))
            else:
                log('Empty dataframe! Check file')

        return df

    # df_orders = import_and_check_dataframe(orders_file_path, orders_col_list)
    # df_order_items = import_and_check_dataframe(order_items_file_path, order_items_col_list)
    # df_products = import_and_check_dataframe(products_file_path, products_col_list)
    # df_sellers = import_and_check_dataframe(sellers_file_path, sellers_col_list)

    # all_dataframes_with_names = [['orders_dataset', df_orders], 
    #                             ['order_items', df_order_items], 
    #                             ['products', df_products],
    #                             ['sellers', df_sellers]]
    
    all_dataframes_with_names = []
    for i in get_filenames_and_required_columns():
        all_dataframes_with_names.append(import_and_check_dataframe(i[0], i[1]))
        
    return all_dataframes_with_names

if __name__ == "__main__":
    log = info
    get_data(log=log)
