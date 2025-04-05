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

    @contextmanager
    def _fetch_data_dict_generator(
        csv_filepath: Path,
    ) -> Generator[dict[str, list[str]], Any, Any]:
        try:
            split_lines = (
                line for line in csv.reader(open(csv_filepath, encoding="utf-8"))
            )
            columns = next(split_lines)
            pprint(f"INFO: Columns of the fetched CSV file: {columns}")
            data_dict_generator = (
                dict(zip(columns, split_line)) for split_line in split_lines
            )
            yield data_dict_generator
        finally:
            data_dict_generator.close()

    def explore(self):
        with temp_unzip_dir(self.filepath) as temp_dir:
            file_paths_generator = (path for path in temp_dir.glob("*.csv"))
            to_be_selected = {
                index: path for index, path in enumerate(file_paths_generator)
            }
            if not to_be_selected:
                print(f"No .csv files found in the directory: {temp_dir}")
                return

            print("What .csv file do you want to explore?")
            selected_path: Path | None = None
            while True:
                try:
                    pprint(to_be_selected)
                    selected_index = input("Please input file's index: ")
                    selected_index = int(selected_index)
                    selected_path = to_be_selected.get(selected_index, None)
                    if selected_path:
                        break
                    else:
                        print("Invalid index of a file! Try again.")
                except ValueError:
                    logging.exception(
                        f"Selected index of a file is not a number: {selected_index}"
                    )

            print(f"You have selected: {selected_path}")
            with DataPuppy._fetch_data_dict_generator(selected_path) as csv_dicts:
                budgets = (
                    (str(csv_dict["title"]), int(csv_dict["budget"]))
                    for csv_dict in csv_dicts
                    if float(csv_dict["vote_average"]) >= 7
                )
                lowest_budget = min(
                    budgets, key=lambda budget: budget[1]
                )  # sort by budget in (title, budget)
                print(f"A minimum budget of a movie: {lowest_budget}")
