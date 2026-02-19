import sys
import os


def get_file(relative_path) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return str(os.path.join(base_path, relative_path))
