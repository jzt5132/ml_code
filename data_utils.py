"""
This module defines class and methods for machine learning data
"""
from typing import Tuple
from dataclasses import dataclass
from enum import Enum
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from utils import get_logger_handle


logger = get_logger_handle(__name__)

RANDOM_SEED = 42


class MlDataLabel(Enum):
    """
    An Enum class to hold ML data label
    """
    ORIG = 0
    TRAIN = 1
    TEST = 2
    UNKNOWN = 100


class MlDataTransform(Enum):
    """
    An Enum class to hold tranformation label
    """
    NO_TRANSFORM = 0
    DROP_NA = 1
    FILLNA = 2
    UNKNOWN = 100


@dataclass
class MlData:
    """
    A class to hold machine learning data
    """
    X: np.ndarray
    y: np.ndarray
    label: MlDataLabel = MlDataLabel.UNKNOWN
    tranform: MlDataTransform = MlDataTransform.UNKNOWN


def create_train_test_data(pd_df: pd.DataFrame, dependent_val: str,
                           test_size: float) -> Tuple[MlData, MlData, MlData]:
    """
    This function creats train and test data for machine learning.
    """
    X = pd_df.drop(dependent_val, axis=1)
    y = pd_df[dependent_val]
    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_SEED)
    orig_data = MlData(X=X, y=y, label=MlDataLabel.ORIG,
                       tranform=MlDataTransform.NO_TRANSFORM)
    train_data = MlData(X=x_train, y=y_train, label=MlDataLabel.TRAIN,
                        tranform=MlDataTransform.NO_TRANSFORM)
    test_data = MlData(X=x_test, y=y_test, label=MlDataLabel.TEST,
                       tranform=MlDataTransform.NO_TRANSFORM)
    return orig_data, train_data, test_data


if __name__ == "__main__":
    from reader import fetch_data_with_summary
    from utils import log_df_summary
    FILE_PATH = "./data/fulldata.dat"
    SEP_STR = r"\s+"
    df = fetch_data_with_summary(FILE_PATH, SEP_STR)
    log_df_summary(df, logger)
    ml_data_tuple = create_train_test_data(df, "logRc", 0.2)
    logger.info("orig data has %s rows", len(ml_data_tuple[0].y))
    logger.info("train data has %s rows", len(ml_data_tuple[1].y))
    logger.info("test data has %s rows", len(ml_data_tuple[2].y))
