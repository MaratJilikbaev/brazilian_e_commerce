import re
import pandas as pd


def save_dataframe(df: pd.DataFrame, to_file: str, log=None, **kwargs):
    if log:
        log(f'saving {to_file}...')

    if to_file.endswith('.csv'):
        df.to_csv(to_file, **kwargs)
    elif to_file.endswith('.xlsx'):
        df.to_excel(to_file, **kwargs)


def load_dataframe(from_file: str, log=None, **kwargs) -> pd.DataFrame:
    if log:
        log(f'loading {from_file}...')

    if from_file.endswith('.csv'):
        df = pd.read_csv(from_file, **kwargs)
    elif from_file.endswith('.xlsx'):
        df = pd.read_excel(from_file, **kwargs)

    if log:
        log(f'\t\tdf.shape={df.shape}...')
    return df
