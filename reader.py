"""
This module includes helper functions to read csv files
"""
import pandas as pd
from logging_utils import get_logger_handle, log_df_summary, log_table

logger = get_logger_handle(__name__)


def fetch_data_with_summary(file_path: str, sep: str) -> pd.DataFrame:
    """
    This function read a csv file into pandas data frame.
    """
    try:
        pd_df = pd.read_csv(file_path, sep=sep)
    except IOError as ex:
        raise Exception(f"Can not read {file_path}") from ex
    log_df_summary(pd_df, logger)
    return pd_df


if __name__ == "__main__":
    FILE_PATH = "./data/fulldata.dat"
    SEP_STR = "\\s+"
    df = fetch_data_with_summary(FILE_PATH, SEP_STR)
    # df = pd.DataFrame({'a': [np.nan, 2, 3], 'b': [4, 5, np.nan]})
    log_table(df, logger)
    # log_table(clean_data(df), logger)
