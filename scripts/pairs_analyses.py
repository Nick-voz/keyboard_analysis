import sqlite3
from datetime import datetime
from string import ascii_letters
from string import punctuation
from typing import Any
from typing import Literal

import matplotlib.pyplot as plt  # pylint: disable=import-error
import pandas as pd  # pylint: disable=import-error
import seaborn as sns  # pylint: disable=import-error
from env import DB_PATH  # pylint: disable=import-error
from env import MEDIA_ROOT  # pylint: disable=import-error
from env import RUSSIAN_LETTERS  # pylint: disable=import-error

NAME = None
PROMPT = """Chose allowed keys:
ru(0), 
ascii letters(1),
punctuation(2),
ru+punctuation(3),
ascii+punctuation(4)
>>> """


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


def get_filtered_pyres(
    _filter: Literal["asci", "ru", "punctuation", "asci+p", "ru+p"]
):
    global NAME  # pylint: disable=global-statement
    keys_df = load_keys_df()
    if _filter == "asci":
        pyres = get_pyres(keys_df, ascii_letters)
        NAME = "ascii_letters"
    elif _filter == "ru":
        pyres = get_pyres(keys_df, RUSSIAN_LETTERS)
        NAME = "russian"
    elif _filter == "asci+p":
        pyres = get_pyres(keys_df, ascii_letters + punctuation)
        NAME = "ascii_letters+punctuation"
    elif _filter == "ru+p":
        pyres = get_pyres(keys_df, RUSSIAN_LETTERS + punctuation)
        NAME = "russian+punctuation"
    else:
        pyres = get_pyres(keys_df, punctuation)
        NAME = "punctuation"
    return pyres


def prepare_data(pyres):
    """Prepares keypress data for visualization.

    Args:
        pyres: A list of tuples, where each tuple contains a pair of consecutive keypresses.

    Returns:
        pd.DataFrame: A Pandas DataFrame representing a frequency table of keypress pairs,
                      with rows and columns representing the first and second keys respectively,
                      and values representing the frequency of each pair.  The DataFrame is
                      square, containing only keys present in the input data.
    """

    pyres_df = pd.DataFrame(pyres, columns=["first_key", "second_key"])
    frequency_table = pyres_df.pivot_table(
        index="first_key", columns="second_key", aggfunc="size", fill_value=0
    )
    keys = frequency_table.sum(axis=1).index
    return frequency_table.loc[keys, keys]


def create_visualization(filtered_frequency_table, annot=False):
    plt.figure(figsize=(20, 18))
    sns.set_theme(font_scale=1)
    sns.heatmap(
        filtered_frequency_table,
        annot=annot,
        fmt="d",
        cmap="YlGnBu",
        cbar_kws={"label": "Частота"},
    )

    plt.title("Частота пар нажатий клавиш", fontsize=16)

    plt.xlabel("Следующая клавиша", fontsize=12)
    plt.ylabel("Текущая клавиша", fontsize=12)

    plt.yticks(rotation=0)


def save_visalization():
    """Saves the generated heatmap visualization to a PNG file.

    The function saves the currently active Matplotlib figure to a PNG file.
    The filename includes a timestamp and the name of the key set used for the visualization (e.g., "ascii_letters", "russian", etc.).  The file is saved to the directory specified by the `MEDIA_ROOT` environment variable.  After saving, the figure is closed.
    """
    _date = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    file_name = f"{MEDIA_ROOT}pairs_{_date}_{NAME}.png"
    plt.savefig(file_name, bbox_inches="tight")
    plt.close()


def ask_for_filter() -> Literal["asci", "ru", "punctuation", "asci+p", "ru+p"]:
    """Asks the user to choose a filter for keypress data.

    Presents the user with a menu of options for filtering keypress data:
    - ru (Russian letters)
    - asci (ASCII letters)
    - punctuation
    - ru+p (Russian letters and punctuation)
    - asci+p (ASCII letters and punctuation)

    Repeatedly prompts the user until a valid option is selected.

    Returns:
        Literal["asci", "ru", "punctuation", "asci+p", "ru+p"]: The chosen filter.
    """

    options: dict[
        str, Literal["asci", "ru", "punctuation", "asci+p", "ru+p"]
    ] = {
        "0": "ru",
        "1": "asci",
        "2": "punctuation",
        "3": "ru+p",
        "4": "asci+p",
    }
    value = input(PROMPT)
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
