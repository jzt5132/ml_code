"""
The module provides a library of transformers that leverages data 
transformations lbrary in scikit learn, which may 
1. clean (see Preprocessing data)
2. reduce (see Unsupervised dimensionality reduction
3. expand (see Kernel Approximation)
3. generate (see Feature extraction) feature representations.
"""
import pandas as pd


def remove_na(pd_df: pd.DataFrame, is_drop: bool = True) -> pd.DataFrame:
    """
    handling NA in data. Either drop NA and fill NA values
    """
    return pd_df.dropna() if is_drop else pd_df.fillna(pd_df.mean())

