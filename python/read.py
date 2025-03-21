from pathlib import Path
from typing import List  # Added for type hinting

import pandas as pd


def get_data_directory() -> Path:
    """
    Gets the path to the 'data' directory, which is located two levels above the current file.

    Returns:
        Path: The path to the 'data' directory.
    """
    current_directory = Path(__file__)
    data_directory = current_directory.parents[1] / 'data'
    result = data_directory  # Assign result to variable
    return result


def get_subdirectory(subdirectory_name: str) -> Path:
    """
    Gets the path to a subdirectory inside the 'data' directory.

    Args:
        subdirectory_name (str): The name of the subdirectory.

    Returns:
        Path: The path to the specified subdirectory.
    """
    result = get_data_directory() / subdirectory_name  # Assign result to variable
    return result


def get_orders_directory() -> Path:
    result = get_subdirectory('orders')  # Assign result to variable
    return result


def get_users_directory() -> Path:
    result = get_subdirectory('users')  # Assign result to variable
    return result


def get_csvs(directory: Path) -> List[Path]:  # Updated type hint
    """
    Retrieves all CSV files from the specified directory.

    Args:
        directory (Path): The directory to search for CSV files.

    Returns:
        List[Path]: A list of paths to CSV files in the directory.

    Raises:
        NotADirectoryError: If the specified path is not a directory.
    """
    if not directory.is_dir():
        raise NotADirectoryError(f'{directory} is not a directory.')
    csv_paths = directory.iterdir()
    csv_files = [csv for csv in csv_paths if csv.suffix == '.csv']
    result = csv_files  # Assign result to variable
    return result


def merge_csvs(csv_files: List[Path]) -> pd.DataFrame:  # Updated type hint
    """
    Merges multiple CSV files into a single pandas DataFrame.

    Args:
        csv_files (List[Path]): A list of paths to CSV files.

    Returns:
        pd.DataFrame: A DataFrame containing the merged data from all CSV files.
    """
    df = pd.concat(
        [pd.read_csv(csv, sep=';') for csv in csv_files], ignore_index=True
    )
    result = df  # Assign result to variable
    return result


def example():
    """
    Example usage:
    - Reads and merges CSV files from 'orders' and 'users' directories.
    - Prints the first few rows of each merged DataFrame.
    """
    orders_directory = get_orders_directory()
    orders_csvs = get_csvs(orders_directory)
    orders_df = merge_csvs(orders_csvs)
    print(orders_df.head())

    users_directory = get_users_directory()
    users_csvs = get_csvs(users_directory)
    users_df = merge_csvs(users_csvs)
    print(users_df.head())


example()
