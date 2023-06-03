import pandas as pd
import numpy as np 


def transform(data, **kwargs): 
    CATEGORY_COLUMNS = ["Type", "Breed1", "Breed2", "Gender", "Color1", "Color2", "Color3",
                        "MaturitySize", "FurLength", "Vaccinated", "Dewormed", "Sterilized", "Health", "State"]

    data["Description"] = data["Description"].fillna("")
    data["desc_length"] = data["Description"].str.len()
    data["desc_words"] = data["Description"].apply(lambda x: len(x.split()))
    data["average_word_length"] = data["desc_length"] / data["desc_words"]

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
