import logging
import pandas as pd 
from tabulate import tabulate

def get_logger_handle(name: str, level = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger


def log_table(df: pd.DataFrame, logger: logging.Logger, round_digits: int = 3) -> None:
    pretty_df = tabulate(df.round(round_digits), headers='keys', tablefmt='psql')
    logger.info(pretty_df)

def log_df_summary(df: pd.DataFrame, logger: logging.Logger, n_row_print: int = 10) -> None:
    logger.info(f"================================= Data summary =================================")
    logger.info(f"Data frame has {df.shape[0]} rows and {df.shape[1]} columns")
    logger.info(f"\nSampling {n_row_print} rows of data")
    log_table(df.sample(n=n_row_print), logger)
    logger.info(f"\nStatistics of each column of data ")
    log_table(df.describe(), logger, round_digits=2)
    logger.info(f"\nRows with NAN in any column")
    log_table(df[df.isna().any(axis=1)], logger)
    logger.info(f"============================ Done with data summary ============================")
