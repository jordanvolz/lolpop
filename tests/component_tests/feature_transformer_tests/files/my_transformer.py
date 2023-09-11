from sklearn.preprocessing import OneHotEncoder
import pandas as pd


class MyTransformer():

    def fit(self, config, X_data, y_data, *args, **kwargs):
        categorical_cols = config.get("categorical_columns")
        #encode categories
        self.ft = OneHotEncoder(handle_unknown="ignore")
        self.ft.fit(X_data[categorical_cols])
        return self.ft

    def transform(self, config, data, *args, **kwargs):
        categorical_cols = config.get("categorical_columns")
        transformed_data = self.ft.transform(data[categorical_cols])
        transformed_df = pd.DataFrame(
            transformed_data.toarray(), columns=self.ft.get_feature_names_out())
        data_out = pd.concat(
            [transformed_df, data.drop(columns=categorical_cols)], axis=1)
        return data_out
