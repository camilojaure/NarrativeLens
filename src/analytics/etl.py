#!/usr/bin/env python3
"""
ETL: TikTok Top-Likes Ads  ->  two CSV artefacts
------------------------------------------------
Reads   ../../data/datasets/NarrativeLens.tiktok_ads_us_toplikes.json
Writes  ../../data/datasets/detail_ugc_analysis.csv
        ../../data/datasets/tiktok_topads_clean.csv
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

import pandas as pd

RAW_JSON = Path("data/datasets/NarrativeLens.tiktok_ads_us_toplikes.json")
CLEAN_CSV = Path("data/datasets/tiktok_topads_clean.csv")
UGC_CSV = Path("data/datasets/detail_ugc_analysis.csv")


# ---------- helper extractors ----------
def extract_video_info(v: Dict[str, Any]) -> pd.Series:
    return pd.Series({"duration": v.get("duration"),
                      "height": v.get("height"),
                      "width": v.get("width")})


def extract_industry(ind: Dict[str, Any]) -> pd.Series:
    return pd.Series({"industry_parent": ind.get("parent", {}).get("value"),
                      "industry_child": ind.get("child", {}).get("value")})


def extract_objective(obj: Dict[str, Any]) -> pd.Series:
    return pd.Series({"objective_value": obj.get("value")})


def extract_creative(cf: Dict[str, Any]) -> pd.Series:
    return pd.Series({
        "creative_theme": cf.get("creative_theme"),
        "creative_concept": cf.get("creative_concept"),
        "format_production_style": cf.get("format_production_style"),
        "talent_type": cf.get("talent_type"),
        "demographic_representation": cf.get("demographic_representation"),
        "audience_focus": cf.get("audience_focus"),
        "campaign_objective": cf.get("campaign_objective"),
    })


# ---------- pipeline steps ----------
def load_raw(path: Path) -> pd.DataFrame:
    with path.open("r") as fp:
        data = json.load(fp)
    df = pd.DataFrame(data)
    logging.info("Loaded %d rows from %s", len(df), path)
    return df


def flatten_nested(df: pd.DataFrame) -> pd.DataFrame:
    return pd.concat(
        [
            df,
            df["video_info"].apply(extract_video_info),
            df["industry"].apply(extract_industry),
            df["objective"].apply(extract_objective),
            df["creative_features"].apply(extract_creative),
        ],
        axis=1,
    )


def save_detail_ugc(df: pd.DataFrame) -> None:
    cols = {"id", "detail_analysis", "ugc_explanation"}
    if cols.issubset(df.columns):
        UGC_CSV.parent.mkdir(parents=True, exist_ok=True)
        df[list(cols)].to_csv(UGC_CSV, index=False)
        logging.info("Saved UGC detail to %s", UGC_CSV)


def build_clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    initial_rows = len(df)
    df = df.drop_duplicates(subset=["id"], keep="first")
    logging.info("Dropped %d duplicate rows", initial_rows - len(df))

    drop_cols = [
        "video_info", "industry", "tag", "objective", "video_name", "_id",
        "favorite", "is_search", "scrap_datetime", "creative_features",
        "industry_key", "objective_key", "detail_analysis", "ugc_explanation",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    df = df.dropna().reset_index(drop=True)
    logging.info("After cleaning: %d rows x %d columns", *df.shape)
    return df


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.info("ETL started")

    raw_df = load_raw(RAW_JSON)
    flat_df = flatten_nested(raw_df)

    save_detail_ugc(flat_df)

    tidy_df = build_clean_dataset(flat_df)
    CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    tidy_df.to_csv(CLEAN_CSV, index=False)
    logging.info("Saved clean data to %s (%.1f MB)",
                 CLEAN_CSV, CLEAN_CSV.stat().st_size / 1e6)

    logging.info("ETL finished")


if __name__ == "__main__":
    main()