import pandas as pd
import numpy as np


def transform(data, **kwargs):
    CATEGORY_COLUMNS = ["Sex"]
    NUMERICAL_COLUMNS = ["Length", "Diameter", "Height", "Weight", "Shucked Weight", "Viscera Weight", "Shell Weight"]

    #encode categories
    data[CATEGORY_COLUMNS] = data[CATEGORY_COLUMNS].astype(str)
    for col in CATEGORY_COLUMNS:
        _, indexer = pd.factorize(data[col], sort=True)
        data[col] = indexer.get_indexer(data[col])

    return data
