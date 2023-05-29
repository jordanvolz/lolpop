import pandas as pd


def transform(data, **kwargs):

    data['Period'] = pd.to_datetime(data['Period'], format='%d.%m.%Y')

    return data
