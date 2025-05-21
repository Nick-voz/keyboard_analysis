import sqlite3
from collections import Counter

import pandas as pd
from env import DB_PATH
from pandas.core.frame import Index

MINIMAL_VALUE = 1


def connect_to_database(db_path):
    """Establish database connection"""
    return sqlite3.connect(db_path)


def fetch_keys_from_db(cursor):
    """Fetch all keys from the database"""
    cursor.execute("SELECT key FROM keypress")
    return cursor.fetchall()


def get_total_keypresses(cursor):
    """Get total number of keypresses"""
    cursor.execute("SELECT count(*) FROM keypress")
    return cursor.fetchall()[0][0]


def convert_to_key_list(keys):
    """Convert database results to list of keys"""
    return [key[0] for key in keys if key[0]]


def calculate_frequency(key_list):
    """Calculate frequency of each key"""
    return Counter(key_list)


def filter_minimal_frequency(frequency_data, minimal_value):
    """Filter frequencies below minimal value"""
    return [e for e in frequency_data if e[1] >= minimal_value]


def create_frequency_dataframe(key_frequency, total_count):
    """Create pandas DataFrame from frequency data with percentage"""
    data = {"Key": [], "Frequency": [], "Percentage": []}

    for key, freq in key_frequency.items():
        percentage = (freq / total_count) * 100
        data["Key"].append(key)
        data["Frequency"].append(freq)
        data["Percentage"].append(f"{percentage:.2f}%")

    df = pd.DataFrame(data)
    return df.sort_values(by="Frequency", ascending=False)


def display_frequency_table(df):
    """Display formatted frequency table"""
    # Set display options for better visualization
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.colheader_justify", "center")

    print("\nKey Frequency Analysis:")
    print("=" * 50)
    print(df.to_string(index=False))
    print("=" * 50)


def analyze_key_frequency(db_path=DB_PATH):
    """Perform statistical analysis of key frequencies"""
    with connect_to_database(db_path) as db:
        cursor = db.cursor()
        keys = fetch_keys_from_db(cursor)
        total_count = get_total_keypresses(cursor)

    key_list = convert_to_key_list(keys)
    key_frequency = calculate_frequency(key_list)

    # Create DataFrame with frequency data
    df = create_frequency_dataframe(key_frequency, total_count)

    # Filter by minimal value if needed
    df = df[df["Frequency"] >= MINIMAL_VALUE]

    # Display the formatted table
    display_frequency_table(df)

    # Additional summary statistics
    print("\nSummary Statistics:")
    print(f"Total keypresses: {total_count}")
    print(f"Unique keys: {len(df)}")
    print(f"Most frequent key: {df.iloc[0]['Key']} ({df.iloc[0]['Frequency']} times)")
    print(
        f"Least frequent key: {df.iloc[-1]['Key']} ({df.iloc[-1]['Frequency']} times)"
    )


if __name__ == "__main__":
    analyze_key_frequency()
