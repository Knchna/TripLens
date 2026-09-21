"""
TripLens - Package Data Preprocessing
Joins the raw multi-sheet workbook (Packages, Itinerary_Days, Inclusions,
Exclusions, Accommodation) into one structured JSON file per package,
keyed by package_id.

Rule followed: no fabricated fields. Reviews/ratings/trust data do not
exist in the source workbook, so they are explicitly marked unavailable
rather than invented.
"""

import json
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("preprocessing")

RAW_PATH = Path("data/raw/Package_Details_India_final_.xlsx")
OUT_PATH = Path("data/processed/packages.json")


def load_sheet(xls, sheet_name):
    """Every sheet has a human-readable description row right after the
    header (row index 1), which we drop, then we drop rows with no
    package_id (blank template rows)."""
    df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=[1])
    df = df.dropna(subset=["package_id"])
    return df


def group_by_package(df, group_cols_as):
    """Turn a flat per-row sheet into {package_id: [row_dict, row_dict, ...]}"""
    grouped = {}
    for pid, sub in df.groupby("package_id"):
        records = sub.drop(columns=["package_id"]).to_dict(orient="records")
        # Drop NaN values inside each record so we don't ship "NaN" into the API
        cleaned = [
            {k: v for k, v in rec.items() if pd.notna(v)}
            for rec in records
        ]
        grouped[pid] = cleaned
    return grouped


def main():
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Expected dataset at {RAW_PATH} — copy your xlsx there first."
        )

    log.info("Loading workbook: %s", RAW_PATH)
    xls = pd.ExcelFile(RAW_PATH)

    packages_df = load_sheet(xls, "Packages")
    itinerary_df = load_sheet(xls, "Itinerary_Days")
    inclusions_df = load_sheet(xls, "Inclusions")
    exclusions_df = load_sheet(xls, "Exclusions")
    accommodation_df = load_sheet(xls, "Accommodation")

    log.info("Packages: %d rows", len(packages_df))
    log.info("Itinerary days: %d rows", len(itinerary_df))

    itinerary_by_pkg = group_by_package(itinerary_df, "package_id")
    inclusions_by_pkg = group_by_package(inclusions_df, "package_id")
    exclusions_by_pkg = group_by_package(exclusions_df, "package_id")
    accommodation_by_pkg = group_by_package(accommodation_df, "package_id")

    packages = []
    for _, row in packages_df.iterrows():
        pid = row["package_id"]

        record = {k: v for k, v in row.to_dict().items() if pd.notna(v)}
        record["package_id"] = pid

        # Sort itinerary days by day_number if present
        days = itinerary_by_pkg.get(pid, [])
        days_sorted = sorted(days, key=lambda d: d.get("day_number", 0))
        record["itinerary"] = days_sorted if days_sorted else None
        record["itinerary_available"] = bool(days_sorted)

        record["inclusions"] = [
            item.get("inclusion_item") for item in inclusions_by_pkg.get(pid, [])
            if item.get("inclusion_item")
        ]
        record["exclusions"] = [
            item.get("exclusion_item") for item in exclusions_by_pkg.get(pid, [])
            if item.get("exclusion_item")
        ]
        record["accommodation"] = accommodation_by_pkg.get(pid, [])

        # Explicit "not available" rather than fabricated review/trust data
        record["reviews_available"] = False
        record["rating"] = None
        record["total_reviews"] = None
        record["trust_insights"] = None

        packages.append(record)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(packages, f, ensure_ascii=False, indent=2, default=str)

    log.info("Wrote %d packages to %s", len(packages), OUT_PATH)


if __name__ == "__main__":
    main()
