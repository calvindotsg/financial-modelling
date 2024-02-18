import pandas as pd


def read_ticker_symbols(file_path: str, ticker_column: str) -> list[str]:
    """
    Read ticker symbols from a CSV file.

    Parameters
    ----------
    file_path: str
        The path to the CSV file.
    ticker_column: str
        The header of the column containing the ticker symbols.

    Returns
    -------
    list
        A list of ticker symbols extracted from the specified column in the CSV file.

    Notes
    -----
    1. Rationale
        This function reads ticker symbols from a CSV file, providing flexibility in
        specifying the file path and the column header containing the ticker symbols.
        The function uses polars to efficiently handle large CSV files and extract
        the desired information.

    2. Implementation Details
        - The CSV file is read into a LazyFrame using pl.scan_csv().
        - The LazyFrame is materialized into a DataFrame using df.collect().
        - Ticker symbols are extracted from the specified column and returned as a list.

    """
    # Read the CSV file
    df: pd.DataFrame = pd.read_csv(str(file_path))

    # Extract the ticker symbols
    ticker_symbols: list[str] = df[ticker_column].tolist()

    return ticker_symbols
