import os
import pandas as pd
from modules.utils2 import normalize_names

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "ReporterName": "reporter",
        "ReporterISO3": "reporter_iso3",
        "PartnerName": "partner",
        "PartnerISO3": "partner_iso3",
        "Year": "year",
        "ProductCode": "hs4",
        "TradeFlowName": "flow",
        "TradeFlowCode": "flow_code",
        "TradeValue in 1000 USD": "value_kusd"
    }
    
    # Apply rename
    df = df.rename(columns=rename_map)
    
    # Drop unwanted
    drop_cols = ["NetWeight in KGM", "Quantity", "QtyUnit", "netweight_kgm", "qty", "qty_unit"]
    df = df.drop(columns=drop_cols, errors="ignore")
    
    # Normalize Names
    df = normalize_names(df)
    
    # Types
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors='coerce').fillna(0).astype(int)
    if "hs4" in df.columns:
        df["hs4"] = df["hs4"].astype(str)
    if "value_kusd" in df.columns:
        df["value_kusd"] = pd.to_numeric(df["value_kusd"], errors='coerce').fillna(0)
        
    return df

def load_concat(data_dir: str, files: list) -> pd.DataFrame:
    dfs = []
    for f in files:
        path = os.path.join(data_dir, f)
        if os.path.exists(path):
            try:
                tmp = pd.read_csv(path)
                tmp = standardize_columns(tmp)
                dfs.append(tmp)
            except Exception as e:
                print(f"Skipping {f}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def load_target_hs_list(data_dir: str) -> list:
    path = os.path.join(data_dir, "HS4 Trade War US China.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df['HS_Code'].astype(str).tolist()
    return []

def load_all_data(data_dir: str):
    """
    Loads all datasets and returns them.
    """
    asean_files = ["ASEAN_15-16.csv", "ASEAN_17-20.csv", "ASEAN_Total 15-16.csv"]
    china_files = ["China_15-16.csv", "China_17-20.csv", "China_Total 15-16.csv", "China_Total 17-20.csv"]
    usa_files = ["USA_15-16.csv", "USA_17-20.csv"]
    
    asean = load_concat(data_dir, asean_files)
    china = load_concat(data_dir, china_files)
    usa = load_concat(data_dir, usa_files)
    
    combined = pd.concat([asean, china, usa], ignore_index=True)
    
    return asean, china, usa, combined