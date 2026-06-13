import pandas as pd
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)


def clean_nav_history():

    df = pd.read_csv(f"{RAW_PATH}/02_nav_history.csv")

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(["amfi_code", "date"])

    df["nav"] = (
        df.groupby("amfi_code")["nav"]
        .transform(lambda x: x.ffill())
    )

    df = df.drop_duplicates()

    df = df[df["nav"] > 0]

    df.to_csv(
        f"{PROCESSED_PATH}/02_nav_history_clean.csv",
        index=False
    )

    print("NAV History cleaned")


def clean_transactions():

    df = pd.read_csv(f"{RAW_PATH}/08_investor_transactions.csv")

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    mapping = {
        "sip": "SIP",
        "SIP": "SIP",
        "lumpsum": "Lumpsum",
        "Lumpsum": "Lumpsum",
        "redemption": "Redemption",
        "Redemption": "Redemption"
    }

    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .map(mapping)
    )

    df = df[df["amount_inr"] > 0]

    valid_kyc = [
        "Verified",
        "Pending",
        "Rejected"
    ]

    if set(df["kyc_status"].unique()) <= set(valid_kyc):
        print("KYC values valid")
    else:
        print("Unexpected KYC values found")

    df.to_csv(
        f"{PROCESSED_PATH}/08_investor_transactions_clean.csv",
        index=False
    )

    print("Transactions cleaned")


def clean_performance():

    df = pd.read_csv(
        f"{RAW_PATH}/07_scheme_performance.csv"
    )

    return_cols = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct"
    ]

    for col in return_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    anomalies = df[
        (df["return_1yr_pct"] > 100)
        | (df["return_1yr_pct"] < -100)
    ]

    print(
        f"Anomalies Found: {len(anomalies)}"
    )

    df = df[
        (df["expense_ratio_pct"] >= 0.1)
        & (df["expense_ratio_pct"] <= 2.5)
    ]

    df.to_csv(
        f"{PROCESSED_PATH}/07_scheme_performance_clean.csv",
        index=False
    )

    print("Performance cleaned")


def copy_remaining_files():

    files = [
        "01_fund_master.csv",
        "03_aum_by_fund_house.csv",
        "04_monthly_sip_inflows.csv",
        "05_category_inflows.csv",
        "06_industry_folio_count.csv",
        "09_portfolio_holdings.csv",
        "10_benchmark_indices.csv"
    ]

    for file in files:

        df = pd.read_csv(
            f"{RAW_PATH}/{file}"
        )

        df.to_csv(
            f"{PROCESSED_PATH}/{file.replace('.csv','_clean.csv')}",
            index=False
        )


if __name__ == "__main__":

    clean_nav_history()

    clean_transactions()

    clean_performance()

    copy_remaining_files()

    print("All cleaned files saved")