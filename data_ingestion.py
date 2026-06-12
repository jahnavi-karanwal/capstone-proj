import pandas as pd
import os

DATA_PATH = "data/raw"


def load_dataset(file_path):
    return pd.read_csv(file_path)


def print_dataset_summary(df, filename):
    print("\n" + "=" * 60)
    print(f"Dataset: {filename}")
    print("=" * 60)

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())


def load_all_datasets():
    for file in os.listdir(DATA_PATH):

        if file.endswith(".csv"):

            file_path = os.path.join(DATA_PATH, file)

            df = load_dataset(file_path)

            print_dataset_summary(df, file)


if __name__ == "__main__":
    load_all_datasets()