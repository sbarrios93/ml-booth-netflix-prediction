from src.parse_data import parse_combined_data, parse_qualifying_data, generate_prediction_data


if __name__ == "__main__":

    # first we need to load the data
    parse_combined_data(force=False)
    parse_qualifying_data(force=False)
    # generate_prediction_data(force=True)
