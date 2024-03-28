import pandas as pd
from pandas._libs.internals import defaultdict
from unidecode import unidecode
from collections.abc import Callable
import re
from typing import Optional
import uuid
import random
from numbers import Number


# convert a csv into utf8 format
def convert_utf8(original_file_path: str, new_file_path: str):
    df = pd.read_csv(original_file_path, converters=defaultdict(lambda i: str))
    for column in df.columns:
        df[column] = df[column].apply(lambda x: unidecode(str(x)))
    df.to_csv(new_file_path, encoding='utf-8')

#########################
# Single Entry Functions#
#########################

# Remove special characters when dealing with words
# transforms removed characters into spaces, removes . and -
def remove_special_for_words(entry: str | Number):
    return re.sub(r"[^a-zA-Z0-9]+", ' ', str(entry))

# Remove special characters when dealing with numbers
# No spaces, does not remove - and .
def remove_special_for_numbers(entry: str | Number):
    return re.sub(r"[^a-zA-Z0-9-.]+", '', str(entry))

# Remove leading and trailing spaces
def truncate(entry: str | Number):
    return str(entry).strip()

# Replace spaces with underscores
def snake_case(entry: str | Number):
    return str(entry).replace(" ", "_")

# Make all letters lowercase
def lower_case(entry: str | Number):
    return str(entry).lower()

def remove_spaces(entry: str | Number):
    return str(entry).replace(" ", "")

# Get a deterministic hash of a string, dependent only on the seed
# (for creating unique id columns which will always be consistent when fed the same data and seed, even if generated at different times)
def deterministic_uuid(entry: str | Number):
    random.seed(str(entry))
    id = uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)
    id = str(id).replace("-", "")
    return id

def cast_to_datetime(entry: str | Number):
    return pd.to_datetime(str(entry))

########################
# DataFrame Functions #
#######################

# Apply a list of functions to the column headers
def clean_headers(df: pd.DataFrame,
                  cleaning_functions_list: list[Callable]) -> pd.DataFrame:
    column_name_map = {item: item for item in df.columns}
    for item in column_name_map:
        for function in cleaning_functions_list:
            column_name_map[item] = function(column_name_map[item])
    df.rename(columns=column_name_map, inplace=True)
    return df


# Apply a list of functions to selected columns
def clean_columns(df: pd.DataFrame,
                  selected_columns: list[str],
                  cleaning_functions_list: list[Callable]) -> pd.DataFrame:
    for col in selected_columns:
        for function in cleaning_functions_list:
            df[col] = df[col].apply(lambda x: function(x))
    return df


# Apply a list of functions to every single entry in the dataframe
def clean_entries(df: pd.DataFrame,
                  cleaning_functions_list: list[Callable]) -> pd.DataFrame:
    for function in cleaning_functions_list:
        df = df.apply(lambda x: function(x))
        return df


def cast_data_types(df: pd.DataFrame, names_to_types: dict) -> pd.DataFrame:
    return df.astype(names_to_types)


# Create a unique index column by taking a deterministic hash of values in selected identifier columns
def set_unique_index(df: pd.DataFrame, columns_to_hash: list[str], index_name="id",
                     index_length_limit: Optional[int] = None):
    df[index_name] = list(
        map(lambda x: deterministic_uuid(''.join([str(col_value) for col_value in x]))[0:index_length_limit],
            df[columns_to_hash].values))
    df.set_index(index_name, inplace=True)
    return df
