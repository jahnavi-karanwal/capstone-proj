import pandas as pd
from sqlalchemy import create_engine, text

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

engine = create_engine("sqlite:///bluestock_mf.db")

# -----------------------------
# EXECUTE SCHEMA.SQL
# -----------------------------

with open("sql/schema.sql", "r") as file:
    schema_sql = file.read()

with engine.begin() as conn:

    raw_conn = conn.connection

    raw_conn.executescript(schema_sql)

print("Schema created successfully.")

# -----------------------------
# LOAD DIM_FUND
# -----------------------------

fund_df = pd.read_csv(
    "data/processed/01_fund_master_clean.csv"
)

dim_fund = fund_df[
    [
        "amfi_code",
        "fund_house",
        "scheme_name",
        "category",
        "sub_category",
        "risk_category",
    ]
].drop_duplicates()

dim_fund.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False,
)

print("dim_fund loaded")

# -----------------------------
# LOAD DIM_DATE
# -----------------------------

nav_df = pd.read_csv(
    "data/processed/02_nav_history_clean.csv"
)

aum_df = pd.read_csv(
    "data/processed/03_aum_by_fund_house_clean.csv"
)

txn_df = pd.read_csv(
    "data/processed/08_investor_transactions_clean.csv"
)

benchmark_df = pd.read_csv(
    "data/processed/10_benchmark_indices_clean.csv"
)

all_dates = pd.concat(
    [
        pd.to_datetime(nav_df["date"]),
        pd.to_datetime(aum_df["date"]),
        pd.to_datetime(txn_df["transaction_date"]),
        pd.to_datetime(benchmark_df["date"]),
    ]
)

all_dates = pd.DataFrame(
    {"date": all_dates.drop_duplicates()}
)

all_dates["year"] = all_dates["date"].dt.year
all_dates["month"] = all_dates["date"].dt.month
all_dates["quarter"] = all_dates["date"].dt.quarter

all_dates.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False,
)

print("dim_date loaded")

# -----------------------------
# FETCH DIMENSIONS
# -----------------------------

fund_lookup = pd.read_sql(
    """
    SELECT fund_key, amfi_code
    FROM dim_fund
    """,
    engine,
)

date_lookup = pd.read_sql(
    """
    SELECT date_key, date
    FROM dim_date
    """,
    engine,
)

date_lookup["date"] = pd.to_datetime(
    date_lookup["date"]
)

# -----------------------------
# FACT_NAV
# -----------------------------

nav_df["date"] = pd.to_datetime(nav_df["date"])

fact_nav = nav_df.merge(
    fund_lookup,
    on="amfi_code",
)

fact_nav = fact_nav.merge(
    date_lookup,
    on="date",
)

fact_nav = fact_nav[
    [
        "fund_key",
        "date_key",
        "nav",
    ]
]

fact_nav.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False,
)

print("fact_nav loaded")

# -----------------------------
# FACT_TRANSACTIONS
# -----------------------------

txn_df["transaction_date"] = pd.to_datetime(
    txn_df["transaction_date"]
)

fact_txn = txn_df.merge(
    fund_lookup,
    on="amfi_code",
)

fact_txn = fact_txn.merge(
    date_lookup,
    left_on="transaction_date",
    right_on="date",
)

fact_txn = fact_txn[
    [
        "fund_key",
        "date_key",
        "amount_inr",
        "transaction_type",
    ]
]

fact_txn.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False,
)

print("fact_transactions loaded")

# -----------------------------
# FACT_PERFORMANCE
# -----------------------------

perf_df = pd.read_csv(
    "data/processed/07_scheme_performance_clean.csv"
)

fact_perf = perf_df.merge(
    fund_lookup,
    on="amfi_code",
)

fact_perf = fact_perf[
    [
        "fund_key",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "expense_ratio_pct",
    ]
]

fact_perf.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False,
)

print("fact_performance loaded")

# -----------------------------
# FACT_AUM
# -----------------------------

aum_df["date"] = pd.to_datetime(
    aum_df["date"]
)

fact_aum = aum_df.merge(
    date_lookup,
    on="date",
)

fact_aum = fact_aum[
    [
        "date_key",
        "fund_house",
        "aum_crore",
    ]
]

fact_aum.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False,
)

print("fact_aum loaded")

# -----------------------------
# VERIFY COUNTS
# -----------------------------

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum",
]

for table in tables:

    count = pd.read_sql(
        f"SELECT COUNT(*) AS cnt FROM {table}",
        engine,
    )

    print(
        f"{table}: {count['cnt'][0]} rows"
    )

print("Database loading completed.")