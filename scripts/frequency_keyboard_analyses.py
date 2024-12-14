import sqlite3
from collections import Counter

import matplotlib.pyplot as plt  # pylint: disable=import-error
import pandas as pd  # pylint: disable=import-error
from pandas.core.frame import Index  # pylint: disable=import-error

MINIMAL_VALUE = 1
from env import DB_PATH


def visual_analyze_key_frequency(db_path=DB_PATH):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()

        cursor.execute("SELECT key FROM keypress")
        keys = cursor.fetchall()

    key_list = [key[0] for key in keys]
    key_frequency = Counter(key_list)

    axes = Index(["Key", "Frequency"])
    df = pd.DataFrame(key_frequency.items(), columns=axes)
    df = df.sort_values(by="Frequency", ascending=False)

    print("Key Frequency Analysis:")

    plt.figure(figsize=(100, 5))
    plt.bar(df["Key"], df["Frequency"], color="skyblue")
    plt.title("Key Frequency")
    plt.xlabel("Key")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def analyze_key_frequency(db_path=DB_PATH):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()

        cursor.execute("SELECT key FROM keypress")
        keys = cursor.fetchall()
        cursor.execute("SELECT count(*) FROM keypress")
        count = cursor.fetchall()[0][0]

    key_list = [key[0] for key in keys]
    key_frequency = Counter(key_list)

    sorted_frequency = key_frequency.most_common()
    sorted_frequency = [e for e in sorted_frequency if e[1] >= MINIMAL_VALUE]

    print("Key Frequency Analysis:")
    for key, frequency in sorted_frequency:
        print(f"{key}: {frequency}: {frequency/count * 100:.2f}%")


analyze_key_frequency()
