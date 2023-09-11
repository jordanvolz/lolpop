import pandas as pd
import numpy as np 


def transform(data, **kwargs): 

    data["Description"] = data["Description"].fillna("")
    data["desc_length"] = data["Description"].str.len()
    data["desc_words"] = data["Description"].apply(lambda x: len(x.split()))
    data["average_word_length"] = data["desc_length"] / data["desc_words"]

    #split data
    rng = np.random.default_rng()
    data["SPLIT"] = rng.choice(["TRAIN", "VALID"], p=[
                            0.8, 0.2], size=len(data))

    return data
