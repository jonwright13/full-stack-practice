import pandas as pd


def import_data(
    fpath: str, sheet_name: str, header: int = 1, exclude_columns: list[str] = []
) -> pd.DataFrame:
    # Import the dataset
    data = pd.read_excel(fpath, sheet_name=sheet_name, header=header)

    # Early return if no exclude columns
    if len(exclude_columns) == 0:
        return data

    # Create a list of columns to keep -> Remove excluded columns
    columns_to_keep = []
    for col in data.columns:
        if col not in exclude_columns:
            columns_to_keep.append(col)

    # Return a DataFrame with only the selected columns
    return data[columns_to_keep]
