"""
This module provides utils functions to logging data
"""

import logging
import pandas as pd
from tabulate import tabulate


def get_logger_handle(name: str, level=logging.DEBUG) -> logging.Logger:
    """
    Construct a logger handle based on name and logging level and return the handle.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger


def log_table(pd_df: pd.DataFrame, logger: logging.Logger,
              round_digits: int = 3) -> None:
    """
    Get pretty table format logging of a dataframe
    """
    pretty_df = tabulate(pd_df.round(round_digits),
                         headers='keys', tablefmt='psql')
    logger.info(pretty_df)


def log_df_summary(pd_df: pd.DataFrame, logger: logging.Logger,
                   n_row_print: int = 10) -> None:
    """
    Log data frame summary including the following info:
    1. Sampling rows of data, defaulted to be 10;
    2. Statistics of each column of data;
    3. Number of rows with NAN
    """
    logger.info(
        "================================= Data summary =================================")
    logger.info(
        f"Data frame has {pd_df.shape[0]} rows and {pd_df.shape[1]} columns")
    logger.info(f"\nSampling {n_row_print} rows of data")
    log_table(pd_df.sample(n=n_row_print), logger)
    logger.info("\nStatistics of each column of data ")
    log_table(pd_df.describe(), logger, round_digits=2)
    logger.info("\nRows with NAN in any column")
    log_table(pd_df[pd_df.isna().any(axis=1)], logger)
    logger.info(
        "============================ Done with data summary ============================")
