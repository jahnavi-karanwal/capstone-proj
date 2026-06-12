import requests
import pandas as pd
import os

SCHEMES = {
    "hdfc_top100": 125497,
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_largecap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}

OUTPUT_FOLDER = "data/raw"


def fetch_nav_data(scheme_code):

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)

    response.raise_for_status()

    return response.json()


def save_nav_to_csv(nav_json, output_file):

    nav_df = pd.DataFrame(nav_json["data"])

    nav_df.to_csv(output_file, index=False)


def download_all_navs():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for fund_name, scheme_code in SCHEMES.items():

        print(f"Fetching {fund_name}...")

        nav_data = fetch_nav_data(scheme_code)

        output_file = f"{OUTPUT_FOLDER}/{fund_name}_nav.csv"

        save_nav_to_csv(nav_data, output_file)

        print(f"Saved: {output_file}")


if __name__ == "__main__":
    download_all_navs()