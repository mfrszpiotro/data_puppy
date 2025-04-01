import csv


class DataPuppy:
    def __init__(self, filepath: str, mode: str = "r", timeout: int = 5):
        self.filepath = filepath
        self.mode = mode
        self.timeout = timeout

    def __enter__(self):
        self.opened_file = open(self.filepath, self.mode)
        return self.opened_file

    def __exit__(self, exc_type, traceback):
        if self.opened_file:
            self.opened_file.close()
