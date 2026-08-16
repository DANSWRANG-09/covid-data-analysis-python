"""
analysis.py
-----------
COVID-19 Global Data Analysis
Entry point: loads + cleans the data (data_cleaning.py), runs exploratory
analysis, saves chart images to outputs/, and writes a text summary
report to outputs/summary_report.txt.

Usage:
    python analysis.py
"""

import matplotlib.pyplot as plt
import pandas as pd

from data_cleaning import merge_datasets

plt.style.use("seaborn-v0_8-darkgrid")
OUTPUT_DIR = "outputs"


def top_countries_by_cases(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return df.nlargest(n, "Confirmed")[["Country/Region", "Confirmed", "Deaths", "Recovered"]]


def plot_top_countries(df: pd.DataFrame, n: int = 10):
    top = top_countries_by_cases(df, n)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["Country/Region"][::-1], top["Confirmed"][::-1], color="#4C72B0")
    ax.set_xlabel("Confirmed Cases")
    ax.set_title(f"Top {n} Countries by Confirmed COVID-19 Cases")
    for i, v in enumerate(top["Confirmed"][::-1]):
        ax.text(v, i, f" {v:,.0f}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/top_countries_by_cases.png", dpi=150)
    plt.close(fig)


def plot_continent_breakdown(df: pd.DataFrame):
    by_continent = (
        df.dropna(subset=["Continent"])
        .groupby("Continent")[["Confirmed", "Deaths", "Recovered"]]
        .sum()
        .sort_values("Confirmed", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(9, 6))
    by_continent["Confirmed"].plot(kind="bar", ax=ax, color="#DD8452")
    ax.set_ylabel("Total Confirmed Cases")
    ax.set_title("Confirmed COVID-19 Cases by Continent")
    ax.set_xlabel("")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/cases_by_continent.png", dpi=150)
    plt.close(fig)


def plot_cfr_vs_recovery(df: pd.DataFrame, min_cases: int = 5000):
    subset = df[df["Confirmed"] >= min_cases]
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(
        subset["Recovery Rate (%)"], subset["Case Fatality Rate (%)"],
        s=subset["Confirmed"] / subset["Confirmed"].max() * 500 + 15,
        alpha=0.6, color="#55A868", edgecolors="white",
    )
    ax.set_xlabel("Recovery Rate (%)")
    ax.set_ylabel("Case Fatality Rate (%)")
    ax.set_title(f"Recovery Rate vs. Fatality Rate (countries with {min_cases:,}+ cases)\nBubble size = total confirmed cases")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/cfr_vs_recovery_rate.png", dpi=150)
    plt.close(fig)


def plot_testing_vs_cases(df: pd.DataFrame):
    subset = df.dropna(subset=["Tests/1M pop", "Cases per 1M Population"])
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(subset["Tests/1M pop"], subset["Cases per 1M Population"],
               alpha=0.6, color="#C44E52", edgecolors="white")
    ax.set_xlabel("Tests per 1M Population")
    ax.set_ylabel("Confirmed Cases per 1M Population")
    ax.set_title("Testing Intensity vs. Reported Case Rate")
    ax.set_xscale("log")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/testing_vs_cases.png", dpi=150)
    plt.close(fig)


def plot_who_region_deaths(df: pd.DataFrame):
    by_region = df.groupby("WHO Region")["Deaths"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(9, 6))
    by_region.plot(kind="barh", ax=ax, color="#8172B2")
    ax.set_xlabel("Total Deaths")
    ax.set_title("Total COVID-19 Deaths by WHO Region")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/deaths_by_who_region.png", dpi=150)
    plt.close(fig)


def build_summary_report(df: pd.DataFrame) -> str:
    total_cases = df["Confirmed"].sum()
    total_deaths = df["Deaths"].sum()
    total_recovered = df["Recovered"].sum()
    global_cfr = total_deaths / total_cases * 100
    global_rr = total_recovered / total_cases * 100

    top5 = top_countries_by_cases(df, 5)
    lowest_cfr = df[df["Confirmed"] >= 5000].nsmallest(5, "Case Fatality Rate (%)")
    highest_cfr = df[df["Confirmed"] >= 5000].nlargest(5, "Case Fatality Rate (%)")

    lines = [
        "COVID-19 GLOBAL DATA ANALYSIS - SUMMARY REPORT",
        "=" * 50,
        f"Countries analyzed: {df.shape[0]}",
        f"Global confirmed cases: {total_cases:,.0f}",
        f"Global deaths: {total_deaths:,.0f}",
        f"Global recovered: {total_recovered:,.0f}",
        f"Global case fatality rate: {global_cfr:.2f}%",
        f"Global recovery rate: {global_rr:.2f}%",
        "",
        "Top 5 countries by confirmed cases:",
    ]
    for _, row in top5.iterrows():
        lines.append(f"  - {row['Country/Region']}: {row['Confirmed']:,.0f} cases, {row['Deaths']:,.0f} deaths")

    lines.append("")
    lines.append("Lowest case fatality rate (countries with 5,000+ cases):")
    for _, row in lowest_cfr.iterrows():
        lines.append(f"  - {row['Country/Region']}: {row['Case Fatality Rate (%)']}%")

    lines.append("")
    lines.append("Highest case fatality rate (countries with 5,000+ cases):")
    for _, row in highest_cfr.iterrows():
        lines.append(f"  - {row['Country/Region']}: {row['Case Fatality Rate (%)']}%")

    return "\n".join(lines)


def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = merge_datasets()

    plot_top_countries(df)
    plot_continent_breakdown(df)
    plot_cfr_vs_recovery(df)
    plot_testing_vs_cases(df)
    plot_who_region_deaths(df)

    report = build_summary_report(df)
    with open(f"{OUTPUT_DIR}/summary_report.txt", "w") as f:
        f.write(report)

    print(report)
    print(f"\nCharts saved to '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
