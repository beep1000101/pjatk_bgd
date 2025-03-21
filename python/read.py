from pathlib import Path

import pandas as pd


def get_data_directory() -> Path:
    """
    Gets the path to the 'data' directory, which is located two levels above the current file.

    Returns:
        Path: The path to the 'data' directory.
    """
    current_directory = Path(__file__)
    data_directory = current_directory.parents[1] / 'data'
    return data_directory


def get_orders_directory() -> Path:
    """
    Gets the path to the 'orders' directory inside the 'data' directory.

    Returns:
        Path: The path to the 'orders' directory.
    """
    orders_directory = get_data_directory() / 'orders'
    return orders_directory


def get_users_directory() -> Path:
    """
    Gets the path to the 'users' directory inside the 'data' directory.

    Returns:
        Path: The path to the 'users' directory.
    """
    users_directory = get_data_directory() / 'users'
    return users_directory


def get_csvs(directory: Path) -> list:
    """
    Retrieves all CSV files from the specified directory.

    Args:
        directory (Path): The directory to search for CSV files.

    Returns:
        list: A list of paths to CSV files in the directory.

    Raises:
        NotADirectoryError: If the specified path is not a directory.
    """
    if not directory.is_dir():
        raise NotADirectoryError(f'{directory} is not a directory.')
    csv_paths = directory.iterdir()
    csv_files = [csv for csv in csv_paths if csv.suffix == '.csv']
    return csv_files


def merge_csvs(csv_files: list) -> pd.DataFrame:
    """
    Merges multiple CSV files into a single pandas DataFrame.

    Args:
        csv_files (list): A list of paths to CSV files.

    Returns:
        pd.DataFrame: A DataFrame containing the merged data from all CSV files.
    """
    df = pd.concat(
        [pd.read_csv(csv, sep=';') for csv in csv_files], ignore_index=True
    )
    return df


# example of use
if __name__ == '__main__':
    orders_directory = get_orders_directory()
    orders_csvs = get_csvs(orders_directory)
    orders_df = merge_csvs(orders_csvs)
    print(orders_df.head())

    users_directory = get_users_directory()
    users_csvs = get_csvs(users_directory)
    users_df = merge_csvs(users_csvs)
    print(users_df.head())
