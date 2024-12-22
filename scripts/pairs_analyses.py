import sqlite3
from datetime import date
from datetime import datetime
from datetime import time
from string import ascii_letters
from string import ascii_lowercase
from string import ascii_uppercase
from string import punctuation
from time import sleep
from typing import Any
from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from env import DB_PATH
from env import MEDIA_ROOT
from env import RUSSIAN_LETTERS

NAME = None


def load_keys_df() -> pd.DataFrame:
    connection = sqlite3.connect(DB_PATH)

    query = "SELECT key FROM keypress ORDER BY timestamp"
    _keys_df = pd.read_sql_query(query, connection)

    connection.close()
    return _keys_df


def get_pyres(
    keys_df: pd.DataFrame, allolewd_keys, case_ignore=True
) -> list[tuple[Any, Any]]:
    _pyres = []
    for i in range(len(keys_df) - 1):
        first_key = keys_df.iloc[i]["key"]
        second_key = keys_df.iloc[i + 1]["key"]
        if first_key is None or second_key is None:
            continue

        if first_key not in allolewd_keys:
            continue
        if second_key not in allolewd_keys:
            continue

        if case_ignore:
            _pyres.append((first_key.lower(), second_key.lower()))
            continue
        _pyres.append((first_key, second_key))
    return _pyres


def get_filtered_pyres(filter: Literal["asci", "ru", "punctuation"]):
    global NAME  # pylint: disable=global-statement
    keys_df = load_keys_df()
    if filter == "asci":
        pyres = get_pyres(keys_df, ascii_letters + punctuation)
        NAME = "ascii_letters"
    elif filter == "ru":
        pyres = get_pyres(keys_df, RUSSIAN_LETTERS + punctuation)
        NAME = "russian"
    else:
        pyres = get_pyres(keys_df, punctuation)
        NAME = "punctuation"
    return pyres


def prepare_data(pyres):
    pyres_df = pd.DataFrame(pyres, columns=["first_key", "second_key"])
    frequency_table = pyres_df.pivot_table(
        index="first_key", columns="second_key", aggfunc="size", fill_value=0
    )
    keys = frequency_table.sum(axis=1).index
    return frequency_table.loc[keys, keys]


def create_visualization(filtered_frequency_table):
    plt.figure(figsize=(20, 18))
    sns.set_theme(font_scale=1)
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


def save_visalization():
    _date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    file_name = f"{MEDIA_ROOT}pairs_{_date}_{NAME}.png"
    plt.savefig(file_name, bbox_inches="tight")
    plt.close()


def ask_for_filter() -> Literal["ru", "asci", "punctuation"]:
    options: dict[str, Literal["ru", "asci", "punctuation"]] = {
        "0": "ru",
        "1": "asci",
        "2": "punctuation",
    }
    value = input(
        "Chose allowed keys: ru(0), ascii letters(1), punctuation(2): "
    )
    if value not in options:
        return ask_for_filter()
    return options[value]


def main():
    _filter = ask_for_filter()
    pyres = get_filtered_pyres(_filter)
    create_visualization(prepare_data(pyres))
    save_visalization()


if __name__ == "__main__":
    main()
