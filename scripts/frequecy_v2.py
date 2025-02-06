import sqlite3
from collections import Counter

import matplotlib.pyplot as plt
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


def create_frequency_dataframe(key_frequency):
    """Create pandas DataFrame from frequency data"""
    axes = Index(["Key", "Frequency"])
    df = pd.DataFrame(key_frequency.items(), columns=axes)
    return df.sort_values(by="Frequency", ascending=False)


def plot_frequency_graph(df):
    """Create and display frequency bar plot"""
    plt.figure(figsize=(100, 5))
    plt.bar(df["Key"], df["Frequency"], color="skyblue")
    plt.title("Key Frequency")
    plt.xlabel("Key")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def print_frequency_analysis(sorted_frequency, total_count):
    """Print frequency analysis results"""
    print("Key Frequency Analysis:")
    for key, frequency in sorted_frequency:
        percentage = (frequency / total_count) * 100
        print(f"{key}: {frequency}: {percentage:.2f}%")


def visual_analyze_key_frequency(db_path=DB_PATH):
    """Perform visual analysis of key frequencies"""
    with connect_to_database(db_path) as db:
        cursor = db.cursor()
        keys = fetch_keys_from_db(cursor)

    key_list = convert_to_key_list(keys)
    key_frequency = calculate_frequency(key_list)
    df = create_frequency_dataframe(key_frequency)
    plot_frequency_graph(df)


def analyze_key_frequency(db_path=DB_PATH):
    """Perform statistical analysis of key frequencies"""
    with connect_to_database(db_path) as db:
        cursor = db.cursor()
        keys = fetch_keys_from_db(cursor)
        count = get_total_keypresses(cursor)

    key_list = convert_to_key_list(keys)
    key_frequency = calculate_frequency(key_list)
    sorted_frequency = key_frequency.most_common()
    filtered_frequency = filter_minimal_frequency(
        sorted_frequency, MINIMAL_VALUE
    )
    print_frequency_analysis(filtered_frequency, count)


if __name__ == "__main__":
    analyze_key_frequency()
    visual_analyze_key_frequency()
