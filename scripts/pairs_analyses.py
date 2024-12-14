import sqlite3
from string import ascii_letters
from string import ascii_lowercase
from string import ascii_uppercase
from string import punctuation
from time import sleep
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import time

RUSSIAN_LETTERS_LOWER = "юпхыяеаоиуйэцкьъзшщдлвмстрнгжчб"
RUSSIAN_LETTERS_UPPER = "ЮПХЫЯЕАОИУЙЭЦКЬЪЗШЩДЛВМСТРНГЖЧБ"
RUSSIAN_LETTERS = RUSSIAN_LETTERS_LOWER + RUSSIAN_LETTERS_UPPER


def load_keys_df() -> pd.DataFrame:
    connection = sqlite3.connect("key_presses.db")

    query = "SELECT key FROM keypress ORDER BY timestamp"
    _keys_df = pd.read_sql_query(query, connection)

    connection.close()
    return _keys_df


def get_pyres(
    keys_df: pd.DataFrame, allolewd_keys, case_ignore=False
) -> list[tuple[Any, Any]]:
    _pyres = []
    for i in range(len(keys_df) - 1):
        first_key = keys_df.iloc[i]["key"]
        second_key = keys_df.iloc[i + 1]["key"]

        if first_key not in allolewd_keys:
            continue
        if second_key not in allolewd_keys:
            continue

        if case_ignore:
            _pyres.append((first_key.lower(), second_key.lower()))
            continue
        _pyres.append((first_key, second_key))
    return _pyres


keys_df = load_keys_df()
pyres = get_pyres(keys_df, ascii_letters)
# pyres = get_pyres(keys_df, RUSSIAN_LETTERS)
# pyres = get_pyres(keys_df, RUSSIAN_LETTERS, case_ignore=True)
# pyres = get_pyres(keys_df, punctuation)


pyres_df = pd.DataFrame(pyres, columns=["first_key", "second_key"])

frequency_table = pyres_df.pivot_table(
    index="first_key", columns="second_key", aggfunc="size", fill_value=0
)

top_keys = frequency_table.sum(axis=1).nlargest(30).index

filtered_frequency_table = frequency_table.loc[top_keys, top_keys]

plt.figure(figsize=(20, 18))
sns.set(font_scale=1)
sns.heatmap(
    filtered_frequency_table,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    cbar_kws={"label": "Частота"},
)

plt.title("Частота пар нажатий клавиш", fontsize=16)

plt.xlabel("Следующая клавиша", fontsize=12)
plt.ylabel("Текущая клавиша", fontsize=12)

plt.yticks(rotation=0)


plt.savefig("/Users/nikitavozisow/Desktop/pyres.png", bbox_inches="tight")
# plt.show()
plt.close()
