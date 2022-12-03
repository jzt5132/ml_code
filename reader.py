import pandas as pd 
from utils import get_logger_handle, log_df_summary, log_table

logger = get_logger_handle(__name__)


def fetch_data_with_summary(file_path: str, sep: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, sep=sep)
    except IOError:
        raise Exception(f"Can not read {file_path}.")
    log_df_summary(df, logger)
    return df


def clean_data(df: pd.DataFrame, is_drop: bool = True) -> pd.DataFrame:
    """
    handling NA in data. Either drop NA and fill NA values
    """
    return df.dropna() if is_drop else df.fillna(df.mean())


if __name__ == "__main__":
    import numpy as np
    FILE_PATH = "fulldata.dat"
    SEP_STR = "\s+"
    df = fetch_data_with_summary(FILE_PATH, SEP_STR)
    df = pd.DataFrame({'a': [np.nan, 2, 3], 'b': [4, 5, np.nan]})
    log_table(df, logger)
    log_table(clean_data(df), logger)
