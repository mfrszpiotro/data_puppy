import csv
import shutil
from pprint import pprint
from pathlib import Path
from typing import Any, Generator
from zipfile import ZipFile
import logging
from contextlib import contextmanager


@contextmanager
def temp_unzip_dir(filepath: str) -> Generator[Path, None, None]:
    try:
        TEMP_DIR = Path.cwd() / "temp_zip"
        TEMP_DIR.mkdir()
        with ZipFile(filepath, "r") as zip_reference:
            zip_reference.extractall(TEMP_DIR)
        yield TEMP_DIR
    finally:
        shutil.rmtree(TEMP_DIR)


class DataPuppy:
    def __init__(self, filepath: str):
        self.filepath = filepath
