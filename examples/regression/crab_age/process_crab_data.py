import pandas as pd
import numpy as np


def transform(data, **kwargs):
    rng = np.random.default_rng()
    data["SPLIT"] = rng.choice(["TRAIN", "VALID"], p=[
                            0.8, 0.2], size=len(data))

    return data
