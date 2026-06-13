CREATE TABLE dim_fund (

    fund_key INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER UNIQUE,

    fund_house TEXT,

    scheme_name TEXT,

    category TEXT,

    sub_category TEXT,

    risk_category TEXT
);

CREATE TABLE dim_date (

    date_key INTEGER PRIMARY KEY AUTOINCREMENT,

    date DATE,

    year INTEGER,

    month INTEGER,

    quarter INTEGER
);

CREATE TABLE fact_nav (

    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_key INTEGER,

    date_key INTEGER,

    nav REAL,

    FOREIGN KEY(fund_key)
        REFERENCES dim_fund(fund_key),

    FOREIGN KEY(date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE fact_transactions (

    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_key INTEGER,

    date_key INTEGER,

    amount_inr REAL,

    transaction_type TEXT,

    FOREIGN KEY(fund_key)
        REFERENCES dim_fund(fund_key),

    FOREIGN KEY(date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE fact_performance (

    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_key INTEGER,

    return_1yr_pct REAL,

    return_3yr_pct REAL,

    return_5yr_pct REAL,

    expense_ratio_pct REAL,

    FOREIGN KEY(fund_key)
        REFERENCES dim_fund(fund_key)
);

CREATE TABLE fact_aum (

    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,

    date_key INTEGER,

    fund_house TEXT,

    aum_crore REAL,

    FOREIGN KEY(date_key)
        REFERENCES dim_date(date_key)
);
