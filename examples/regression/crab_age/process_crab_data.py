import pandas as pd
import numpy as np


def transform(data, **kwargs):
    CATEGORY_COLUMNS = ["Sex"]

    #ensure type is categorical for downstream encoding
    data[CATEGORY_COLUMNS] = data[CATEGORY_COLUMNS].astype("category")

    return data
