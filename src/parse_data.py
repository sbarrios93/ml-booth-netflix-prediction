from pathlib import Path

# init vars
HERE = Path(__file__).parent
ROOT = HERE.parent


# directory names
DATA_DIR = "data"
RAW_DATA_DIR = "raw"
PARSED_DATA_DIR = "parsed"

# expected output dirs
DATA_PATH = ROOT / DATA_DIR
RAW_DATA_PATH = DATA_PATH / RAW_DATA_DIR
PARSED_DATA_PATH = DATA_PATH / PARSED_DATA_DIR


def _assert_and_make_dirs():
    assert Path.exists(
        RAW_DATA_PATH
    ), f"raw data directory not found. \n Netflix data should be downloaded in {str(RAW_DATA_PATH)}"
    Path.mkdir(PARSED_DATA_PATH, exist_ok=True)


def parse_combined_data(i=1, force=False):
    """
    The code above does the following:
    1. Reads the combined data file and writes out the movie id and the review to a new file
    2. Each line in the new file is of the following format:
    movie_id,review
    """

    _assert_and_make_dirs()  # make sure directories are present

    def parse_data(i, out_file_path):
        movie_id = "0"  # remove unbounded var warning
        out = open(out_file_path, "w")
        with open(f"data/raw/combined_data_{i}.txt", "r") as f:
            for line in f.readlines():
                if ":" in line:
                    movie_id = line.strip()[:-1]
                out.writelines(movie_id + "," + line)

    out_file = "parsed_combined_data_" + str(i) + ".txt"
    out_file_path = PARSED_DATA_PATH / out_file
    if Path(out_file_path).is_file() and not force:
        print(
            f"File {str(out_file_path)} exists, skipping. If you want to force the file to be created, set force=True"
        )
    else:
        parse_data(i, out_file_path)


def parse_qualifying_data(force=False):
    """
    The code above does the following:
    1. Removes all the special characters from the raw data
    2. Removes the line with the header
    3. Writes the movie_id and the raw data into a new file
    """

    _assert_and_make_dirs()  # make sure directories are present

    def parse_data(out_file_path):
        movie_id = "0"  # remove unbounded var warning
        out = open(str(out_file_path), "w")
        with open("data/raw/qualifying.txt", "r") as f:
            for line in f.readlines():
                if ":" in line:
                    movie_id = line.strip()[:-1]
                    continue
                out.writelines(movie_id + "," + line)

    out_file = "parsed_qualifying" + ".txt"
    out_file_path = PARSED_DATA_PATH / out_file

    if Path(out_file_path).is_file() and not force:
        print(
            f"File {str(out_file_path)} exists, skipping. If you want to force the file to be created, set force=True"
        )
    else:
        parse_data(out_file_path)


def generate_prediction_data(force=False):
    """
    1. It takes the prediction.txt file and parses it into a list of lists,
    where each list is a movie and the list of lists is a list of all the movies
    in the file

    2. It then loops through each movie and writes its id, rating and name to a new
    file called parsed_prediction.txt.
    """

    _assert_and_make_dirs()  # make sure directories are present

    def parse_data(out_file_path):
        movie_id = 0
        out = open(str(out_file_path), "w")
        with open("data/raw/prediction.txt", "r") as f:
            for line in f.readlines():
                row = line.strip().split(",")
                if movie_id != row[0]:
                    movie_id = row[0]
                    out.writelines(movie_id + ":\n")
                out.writelines(row[2] + "\n")

    out_file = "parsed_prediction" + ".txt"
    out_file_path = PARSED_DATA_PATH / out_file

    if Path(out_file_path).is_file() and not force:
        print(
            f"File {str(out_file_path)} exists, skipping. If you want to force the file to be created, set force=True"
        )
    else:
        parse_data(out_file_path)
