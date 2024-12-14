import sqlite3
from time import sleep
from time import time

from pynput.keyboard import Key  # pylint: disable=import-error
from pynput.keyboard import KeyCode  # pylint: disable=import-error
from pynput.keyboard import Listener  # pylint: disable=import-error


def retry(max_attempts: int = 5, backoff_factor: float = 0.1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except sqlite3.Error as e:
                    print(f"Database error occurred: {e}")
                    if attempts < max_attempts - 1:
                        sleep(backoff_factor * (2**attempts))
                    attempts += 1
            raise RuntimeError(
                f"Failed to insert key press data after {attempts} attempts"
            )

        return wrapper

    return decorator


@retry()
def on_press(key: Key | KeyCode | None):
    if key is None:
        return
    timestamp = time()
    if isinstance(key, KeyCode):
        key_char = key.char

    else:
        key_char = str(key)
    with sqlite3.connect("key_presses.db") as db:
        db.execute(
            "INSERT INTO keypress (timestamp, key) VALUES (?, ?)",
            (timestamp, key_char),
        )
        db.commit()


listener = Listener(on_press=on_press)
try:
    listener.start()
    listener.join()
except KeyboardInterrupt:
    listener.stop()
