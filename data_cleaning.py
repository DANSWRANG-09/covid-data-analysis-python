"""
data_cleaning.py
-----------------
Loads the two raw COVID-19 datasets, standardizes country names, cleans
missing/invalid values, and merges them into a single tidy DataFrame
ready for analysis.

Datasets
    data/country_wise_latest.csv  -> case/death/recovery counts per country
    data/worldometer_data.csv     -> population, testing, continent per country
"""

import numpy as np
import pandas as pd

# A handful of countries are spelled differently across the two sources.
# Mapping worldometer_data.csv names -> country_wise_latest.csv names so
# the merge doesn't silently drop them.
NAME_FIXES = {
    "USA": "US",
    "UK": "United Kingdom",
    "S. Korea": "South Korea",
    "UAE": "United Arab Emirates",
    "Ivory Coast": "Cote d'Ivoire",
    "DRC": "Congo (Kinshasa)",
    "Congo": "Congo (Brazzaville)",
    "CAR": "Central African Republic",
    "Czechia": "Czechia",
    "Taiwan": "Taiwan*",
    "Myanmar": "Burma",
    "St. Vincent Grenadines": "Saint Vincent and the Grenadines",
    "Palestine": "West Bank and Gaza",
    "Vatican City": "Holy See",
}


def load_cases_data(path: str = "data/country_wise_latest.csv") -> pd.DataFrame:
    """Load the case/death/recovery dataset."""
    df = pd.read_csv(path)
    df["Country/Region"] = df["Country/Region"].str.strip()
    return df


def load_worldometer_data(path: str = "data/worldometer_data.csv") -> pd.DataFrame:
    """Load the population/testing/continent dataset."""
    df = pd.read_csv(path)
    df["Country/Region"] = df["Country/Region"].str.strip()
    df["Country/Region"] = df["Country/Region"].replace(NAME_FIXES)
    return df


def merge_datasets(cases_path: str = "data/country_wise_latest.csv",
                    worldometer_path: str = "data/worldometer_data.csv") -> pd.DataFrame:
    """Merge the two sources on country name into one tidy DataFrame."""
    cases = load_cases_data(cases_path)
    world = load_worldometer_data(worldometer_path)

    # Keep only the columns from worldometer that add new information
    # (avoid duplicate Confirmed/Deaths columns already in `cases`).
    world_cols = [
        "Country/Region", "Continent", "Population", "TotalTests",
        "Tests/1M pop", "Serious,Critical",
    ]
    world = world[world_cols]

    merged = cases.merge(world, on="Country/Region", how="left")

    # --- Cleaning ---
    # Replace sentinel/invalid numeric values, coerce types
    numeric_cols = merged.select_dtypes(include=[np.number]).columns
    merged[numeric_cols] = merged[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Population/tests genuinely missing for a few micro-states -> leave as NaN,
    # but don't let NaN break rate calculations downstream.
    merged["Population"] = merged["Population"].fillna(np.nan)

    # Derived metrics
    merged["Case Fatality Rate (%)"] = (merged["Deaths"] / merged["Confirmed"] * 100).round(2)
    merged["Recovery Rate (%)"] = (merged["Recovered"] / merged["Confirmed"] * 100).round(2)
    merged["Cases per 1M Population"] = (merged["Confirmed"] / merged["Population"] * 1_000_000).round(1)
    merged["Tests per Confirmed Case"] = (merged["TotalTests"] / merged["Confirmed"]).round(1)

    return merged


if __name__ == "__main__":
    df = merge_datasets()
    print(f"Merged dataset shape: {df.shape}")
    print(f"Countries with missing population/test data: {df['Population'].isna().sum()}")
    print(df.head())
