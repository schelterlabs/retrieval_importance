import pandas as pd

pd.options.mode.chained_assignment = None


def index_consecutive(column, dfs):
    original = set()
    for df in dfs:
        original.update(df[column].unique())

    original_sorted = sorted(list(original))
    mapping = {original_key: index for index, original_key in enumerate(original_sorted)}

    for df in dfs:
        df[column].replace(to_replace=mapping, inplace=True)
