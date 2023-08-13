import pandas as pd
import numpy as np


def transform(data, **kwargs):
    CATEGORY_COLUMNS = ["sex", "smoker", "region"]

    #encode categories
    data[CATEGORY_COLUMNS] = data[CATEGORY_COLUMNS].astype(str)
    for col in CATEGORY_COLUMNS:
        _, indexer = pd.factorize(data[col], sort=True)
        data[col] = indexer.get_indexer(data[col])

    #split data
    rng = np.random.default_rng()
    data["SPLIT"] = rng.choice(["TRAIN", "VALID"], p=[
        0.8, 0.2], size=len(data))

    return data
