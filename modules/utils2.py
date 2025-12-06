import pandas as pd
import numpy as np

ASEAN_ISO3 = ["IDN","MYS","SGP","THA","VNM","BRN","KHM","LAO","MMR","PHL"]

COUNTRY_GROUPS = {
    "ASEAN": set(ASEAN_ISO3),
    "China": {"CHN"},
    "United States": {"USA"},
}

def normalize_names(df: pd.DataFrame) -> pd.DataFrame:
    fix_map = {
        "Viet Nam": "Vietnam",
        "Lao People's Democratic Republic": "Lao PDR",
        "United States of America": "United States",
        " World": "World"
    }
    if "reporter" in df.columns:
        df["reporter"] = df["reporter"].replace(fix_map)
    if "partner" in df.columns:
        df["partner"] = df["partner"].replace(fix_map)
    return df

# --- INTRO MAP DATA BUILDER (Updated) ---
def build_intro_map_data(df: pd.DataFrame):
    """
    Creates a dataframe for coloring the map AND showing Total Trade Value.
    Returns cols: [iso, Group, Total_Trade_Billion, reporter]
    """
    # 1. Aggregate Total Trade by Reporter ISO and Name
    # We grab 'first' reporter name found for the ISO to ensure we have a label
    totals = df.groupby('reporter_iso3').agg({
        'value_kusd': 'sum',
        'reporter': 'first'
    }).reset_index()
    
    totals['Total_Trade_Billion'] = totals['value_kusd'] / 1_000_000
    
    # 2. Define the structural groups
    definitions = []
    definitions.append({'iso': 'USA', 'Group': 'United States'})
    definitions.append({'iso': 'CHN', 'Group': 'China'})
    for iso in ASEAN_ISO3:
        definitions.append({'iso': iso, 'Group': 'ASEAN'})
    
    def_df = pd.DataFrame(definitions)
    
    # 3. Merge Data with Definitions
    merged = pd.merge(def_df, totals, left_on='iso', right_on='reporter_iso3', how='left')
    
    # Fill NaN values
    merged['Total_Trade_Billion'] = merged['Total_Trade_Billion'].fillna(0)
    
    # If reporter name is missing (no data for that ISO), fallback to Group name
    merged['reporter'] = merged['reporter'].fillna(merged['Group'])
    
    # Format for clean hover text
    merged['Formatted_Value'] = merged['Total_Trade_Billion'].apply(lambda x: f"${x:,.1f} B")
    
    return merged[['iso', 'Group', 'Total_Trade_Billion', 'Formatted_Value', 'reporter']]

# --- PIE CHART DATA BUILDER ---
def build_us_import_pie_data(usa_df: pd.DataFrame, hs_list: list, start_year: int, end_year: int):
    """
    Constructs data for US Import Pie Chart: China vs ASEAN vs Other.
    """
    mask = (
        (usa_df['year'] >= start_year) & 
        (usa_df['year'] <= end_year) &
        (usa_df['flow'] == 'Import') &
        (usa_df['hs4'].isin(hs_list))
    )
    df = usa_df[mask]
    
    if df.empty:
        return pd.DataFrame()

    # WLD value check
    wld_val = df[df['partner_iso3'] == 'WLD']['value_kusd'].sum()
    if wld_val == 0:
        wld_val = df[df['partner_iso3'] != 'WLD']['value_kusd'].sum()

    chn_val = df[df['partner_iso3'] == 'CHN']['value_kusd'].sum()
    asean_val = df[df['partner_iso3'].isin(ASEAN_ISO3)]['value_kusd'].sum()
    
    # RoW calculation
    row_val = max(0, wld_val - chn_val - asean_val)
    
    return pd.DataFrame([
        {'Source': 'China', 'Value': chn_val},
        {'Source': 'ASEAN', 'Value': asean_val},
        {'Source': 'Rest of World', 'Value': row_val}
    ])

# --- CIRCUMVENTION METRICS ---

def compute_share_shift(df: pd.DataFrame, hs_filter: list):
    """Calculates market share of China vs ASEAN in US Imports over time."""
    mask = (
        (df['reporter_iso3'] == 'USA') &
        (df['flow'] == 'Import') &
        (df['hs4'].isin(hs_filter))
    )
    sub = df[mask].copy()
    
    stats = []
    for yr in sorted(sub['year'].unique()):
        yr_data = sub[sub['year'] == yr]
        
        wld = yr_data[yr_data['partner_iso3'] == 'WLD']['value_kusd'].sum()
        if wld == 0: wld = yr_data['value_kusd'].sum()
        
        chn = yr_data[yr_data['partner_iso3'] == 'CHN']['value_kusd'].sum()
        asean = yr_data[yr_data['partner_iso3'].isin(ASEAN_ISO3)]['value_kusd'].sum()
        
        if wld > 0:
            stats.append({
                'year': yr,
                'china_share': (chn / wld) * 100,
                'asean_share': (asean / wld) * 100
            })
            
    return pd.DataFrame(stats)

def compute_tii(df: pd.DataFrame, hs_filter: list):
    """Proxy Trade Intensity Index."""
    mask = (
        (df['reporter_iso3'].isin(ASEAN_ISO3)) &
        (df['flow'] == 'Export') &
        (df['hs4'].isin(hs_filter))
    )
    sub = df[mask]
    
    stats = []
    if sub.empty: return pd.DataFrame()

    groups = sub.groupby(['year', 'reporter'])
    for (yr, rep), group in groups:
        total_export = group[group['partner_iso3'] == 'WLD']['value_kusd'].sum()
        us_export = group[group['partner_iso3'] == 'USA']['value_kusd'].sum()
        
        if total_export > 0:
            tii = (us_export / total_export) * 100
            stats.append({'year': yr, 'reporter': rep, 'tii': tii})
            
    return pd.DataFrame(stats)

def compute_tci(df: pd.DataFrame, hs_filter: list):
    """Proxy Trade Complementarity (Volume)."""
    mask = (
        (df['reporter_iso3'].isin(ASEAN_ISO3)) &
        (df['flow'] == 'Export') &
        (df['partner_iso3'] == 'USA') &
        (df['hs4'].isin(hs_filter))
    )
    sub = df[mask]
    if sub.empty: return pd.DataFrame()
    
    return sub.groupby(['year', 'reporter'])['value_kusd'].sum().reset_index().rename(columns={'value_kusd': 'tci'})