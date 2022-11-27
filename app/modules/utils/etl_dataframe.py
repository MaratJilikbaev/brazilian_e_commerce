import io

import pandas as pd

from app.utils.util_dataframe import save_dataframe, load_dataframe
from app.utils.util_json import load_json_from_file, save_to_json_file
from app.utils.util_log import info


def extract_df(json_as_dict, path_in_json):

    def extract_df(json, path):
        for part in path.split('.'):
            json = json[part]

        if json in ('empty_dataframe', ''):
            return pd.DataFrame()
        else:
            return pd.read_json(json)

    df = extract_df(json_as_dict, path_in_json)

    drop_col = 'Unnamed: 0'
    if drop_col in df.columns:
        df.drop(columns=drop_col, inplace=True)

    return df


def extract_all_datasets(request_json_path, response_json_path, log):

    json_as_dict = load_json_from_file(request_json_path, log=log)
    df1 = extract_df(json_as_dict, 'data_load_transform_config.other_assets_raw_dataset.dataframe_in_json')
    df2 = extract_df(json_as_dict, 'data_load_transform_config.portfolio_raw_dataset.dataframe_in_json')
    save_dataframe(df1, 'other_assets.csv', log=log, index=False)
    save_dataframe(df2, 'portfolio.csv', log=log, index=False)

    json_as_dict = load_json_from_file(response_json_path, log=log)
    df1 = extract_df(json_as_dict, 'portf_before')
    df2 = extract_df(json_as_dict, 'portfolio_after')
    df3 = extract_df(json_as_dict, 'portfolio_to_buy')
    df4 = extract_df(json_as_dict, 'portfolio_to_sell')
    save_dataframe(df1, 'portf_before.csv', log=log, index=False)
    save_dataframe(df2, 'portfolio_after.csv', log=log, index=False)
    save_dataframe(df3, 'portfolio_to_buy.csv', log=log, index=False)
    save_dataframe(df4, 'portfolio_to_sell.csv', log=log, index=False)


def inject_dataset(input_json_path, output_json_path, keys_path_in_json, path_to_df, log):

    df = load_dataframe(path_to_df, log=log)

    json_as_dict = load_json_from_file(input_json_path, log=log)

    json_entry = json_as_dict
    keys_path_in_json = keys_path_in_json.split('.')
    if len(keys_path_in_json) > 1:
        for part in keys_path_in_json[:-1]:
            json_entry = json_entry[part]

    json_entry[keys_path_in_json[-1]] = df.to_json(orient="records")

    save_to_json_file(json_as_dict, output_json_path, log=log)


def dataframe_to_bytes(df: pd.DataFrame, log=None, **kwargs):
    if df is None:
        return b''

    to_write = io.BytesIO()
    df.to_excel(to_write, **kwargs)
    to_write.seek(0)
    content = to_write.getvalue()
    return content


if __name__ == '__main__':
    log = info

    extract_all_datasets('data/output/20220801-151931-request.json',
                         'data/output/20220801-151931-response.json',
                         log=log)

    inject_dataset('data/output/20220801-151931-request.json',
                   'fixed-request.json',
                   'data_load_transform_config.portfolio_raw_dataset.dataframe_in_json',
                   'other_assets.csv',
                   log=log)
    pass


