import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from typing import Tuple
import numpy as np
from dataclasses import dataclass
from enum import Enum


RANDOM_SEED = 42

class mlDataLabel(Enum):
    """
    An Enum class to hold ML data label
    """
    ORIG = 0
    TRAIN = 1
    TEST = 2
    UNKNOWN = 100

class mlDataTransform(Enum):
    """
    An Enum class to hold tranformation label
    """
    NO_TRANSFORM = 0
    DROP_NA = 1
    FILLNA = 2
    UNKNOWN = 100
    

@dataclass
class mlData:
    """
    A class to hold machine learning data
    """
    X: np.ndarray
    y: np.ndarray
    label: mlDataLabel = mlDataLabel.UNKNOWN
    tranform: mlDataTransform = mlDataTransform.UNKNOWN
    

def create_train_test_data(df: pd.DataFrame, dependent_val: str, test_size: float) -> Tuple(mlData, mlData, mlData):
    """
    This function creats train and test data for 
    """

    X = df.drop(dependent_val, axis=1)
    y = df[dependent_val]
    mlData
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=RANDOM_SEED)
    return 



"""
Step 1: Assign independent features (those predicting) to X
Step 2: Assign classes (labels/dependent features) to y
Step 3: Divide into training and test setsX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
Step 4: Create the modelsvc = SVC()
Step 5: Fit the modelsvc.fit(X_train, y_train)
Step 6: Predict with the modely_pred = svc.predict(X_test)
Step 7: Test the accuracyaccuracy_score(y_test, y_pred)
"""

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
