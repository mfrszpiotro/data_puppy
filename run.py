from app.pup import DataPuppy
from pathlib import Path


def main():
    dp = DataPuppy(Path.cwd() / "test_data" / "tmdb_movie_archive.zip")
    dp.explore()


if __name__ == "__main__":
    main()
