# COVID-19 Global Data Analysis

A Python data analysis project that cleans, merges, and explores two
COVID-19 datasets to uncover country- and continent-level patterns in
case counts, mortality, recovery, and testing intensity.

## What it does

- **Cleans and merges** two raw CSVs (case/death/recovery counts +
  population/testing/continent data) into one tidy dataset, resolving
  country-name mismatches between sources (e.g. `USA` vs `US`).
- **Derives new metrics**: case fatality rate, recovery rate, cases per
  1M population, and tests per confirmed case.
- **Generates 5 charts** (saved as PNGs) and a text summary report.

## Sample output

![Top countries by cases](outputs/top_countries_by_cases.png)

More charts are generated in `outputs/`: cases by continent, deaths by
WHO region, case-fatality-rate vs. recovery-rate, and testing intensity
vs. reported case rate.

## Key findings (from this snapshot of the data)

- Global case fatality rate: **3.97%**, recovery rate: **57.45%**.
- The US, Brazil, and India account for the largest shares of confirmed
  cases in the dataset.
- Reported case-fatality rates vary enormously by country (from well
  under 1% to over 15% among countries with 5,000+ cases), reflecting
  differences in testing coverage, healthcare capacity, and reporting
  methodology rather than the virus itself.
- Countries that test more per capita tend to report more cases per
  capita — a reminder that "confirmed cases" measures detection as much
  as spread.

Full numbers are in [`outputs/summary_report.txt`](outputs/summary_report.txt)
after running the script.

## Project structure

```
covid19-data-analysis/
├── data/
│   ├── country_wise_latest.csv   # cases, deaths, recovery by country
│   └── worldometer_data.csv      # population, testing, continent by country
├── data_cleaning.py              # load, clean, and merge the two datasets
├── analysis.py                   # EDA, chart generation, summary report
├── outputs/                      # generated charts + summary_report.txt
├── requirements.txt
└── README.md
```

## How to run

```bash
git clone https://github.com/<your-username>/covid19-data-analysis.git
cd covid19-data-analysis
pip install -r requirements.txt
python analysis.py
```

This prints a summary report to the console and writes it, along with
5 chart images, to `outputs/`.

## Tech stack

- **pandas** — data cleaning, merging, aggregation
- **numpy** — numeric operations
- **matplotlib** — visualization

## Data source

Both CSVs are point-in-time COVID-19 snapshots (case/death/recovery
counts and population/testing figures by country), commonly distributed
as a Kaggle dataset. They are included in `data/` so the project runs
out of the box.

## Possible extensions

- Add a time-series version using daily case data instead of a single
  snapshot.
- Build an interactive dashboard (e.g. with Streamlit or Plotly Dash).
- Add unit tests for the cleaning/merge logic in `data_cleaning.py`.

## License

MIT — see [LICENSE](LICENSE).
