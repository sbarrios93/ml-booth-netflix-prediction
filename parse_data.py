import os


def parse_combined_data(i=1):
    out = open(f"data/parsed_combined_data_{i}.txt", "w")
    with open(f"data/combined_data_{i}.txt", "r") as f:
        for l in f.readlines():
            if ":" in l:
                movie_id = l.strip()[:-1]
                continue
            out.writelines(movie_id + "," + l)


def parse_qualifying_data():
    out = open(f"data/parsed_qualifying.txt", "w")
    with open(f"data/qualifying.txt", "r") as f:
        for l in f.readlines():
            if ":" in l:
                movie_id = l.strip()[:-1]
                continue
            out.writelines(movie_id + "," + l)


def generate_prediction_data():
    movie_id = 0
    out = open(f"data/parsed_prediction.txt", "w")
    with open(f"data/prediction.txt", "r") as f:
        for l in f.readlines():
            row = l.strip().split(",")
            if movie_id != row[0]:
                movie_id = row[0]
                out.writelines(movie_id + ":\n")
            out.writelines(row[2] + "\n")


parse_qualifying_data()
