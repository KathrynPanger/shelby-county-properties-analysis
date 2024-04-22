# Convert a data dictionary in condensed format
# to the expanded version that pandas requires as an argument
# for reading csvs with data types in mind
def convert_dictionary(data_dict: dict) -> dict:
    converted_dict = {}
    for key, value in data_dict.items():
        for item in value:
            converted_dict[item] = key
    return converted_dict