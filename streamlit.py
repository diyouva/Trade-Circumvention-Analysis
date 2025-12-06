import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import base64
from pathlib import Path
import streamlit.components.v1 as components

# Import custom modules
from modules.data_load2 import load_all_data, load_target_hs_list
from modules.utils2 import (
    build_intro_map_data,
    build_us_import_pie_data,
    compute_share_shift,
    compute_tii,
    compute_tci
)

# -------------------------------------
# PAGE CONFIG
# -------------------------------------
st.set_page_config(
    page_title="US–China Trade War Dashboard",
    layout="wide"
)

# Load External CSS
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("styles.css not found. Some styling may be missing.")

# -------------------------------------
# CUSTOM CSS FOR TYPOGRAPHY
# -------------------------------------
st.markdown("""
<style>
    /* Main Title: Commanding, Navy Blue */
    .main-title {
        font-family: 'Times New Roman', serif;
        font-size: 3.2em;
        font-weight: 800;
        color: #1e3799; /* Navy Blue */
        margin-bottom: 5px;
        line-height: 1.1;
    }
    
    /* Sub Title: Engaging, Crimson, Serif */
    .sub-title {
        font-family: 'Georgia', serif;
        font-size: 1.5em;
        color: #b71540; /* Crimson */
        margin-top: 5px;
        margin-bottom: 35px;
        font-style: italic;
        font-weight: 500;
        border-bottom: 1px solid #ddd;
        padding-bottom: 15px;
    }
    
    /* Figure Captions: Bold and Conclusive */
    .caption-text {
        font-family: 'Arial', sans-serif;
        font-size: 0.95em;
        font-weight: 600;
        color: #4a69bd;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 25px;
        background-color: #f1f2f6;
        padding: 8px;
        border-radius: 4px;
    }

    /* Journal Body Text: Continuous flow, no sub-headers */
    .journal-text {
        font-family: 'Georgia', serif;
        font-size: 1.15em;
        line-height: 1.8;
        color: #2f3542;
        text-align: justify;
        margin-bottom: 25px;
    }

    /* Highlight Box for Conclusions */
    .highlight-box {
        background-color: #dfe6e9;
        border-left: 5px solid #1e3799;
        padding: 20px;
        border-radius: 4px;
        font-family: 'Georgia', serif;
        font-size: 1.1em;
        line-height: 1.6;
        color: #2d3436;
        margin-top: 30px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------
# HELPER FUNCTIONS & DATA LOADING
# -------------------------------------
def load_base64_image(path):
    try:
        img_bytes = Path(path).read_bytes()
        return base64.b64encode(img_bytes).decode()
    except FileNotFoundError:
        return None

@st.cache_data
def load_data():
    return load_all_data("data")

@st.cache_data
def load_hs():
    return load_target_hs_list("data")

asean_df, china_df, usa_df, all_df = load_data()
target_hs_list = load_hs()

min_year = int(all_df["year"].min()) if not all_df.empty else 2015
max_year = int(all_df["year"].max()) if not all_df.empty else 2020

logo_base64 = load_base64_image("assets/cmu_logo_circular.png")

# -------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------
with st.sidebar:
    if logo_base64:
        st.markdown(
            f'<img src="data:image/png;base64,{logo_base64}" class="cmu-logo">',
            unsafe_allow_html=True
        )

    st.markdown("""
        <div style="text-align:center; font-weight:600; font-size:0.95rem; margin-bottom:0px; padding-bottom:0px; line-height:1.1;">
            Period Filter
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div[data-baseweb="slider"] { margin-top: -20px !important; padding-top: 0px !important; }
        div[data-baseweb="slider"] > div { margin-top: -5px !important; }
        section[data-testid="stSidebar"] > div:first-child { margin-bottom: 5 !important; padding-bottom: 5 !important; }
        </style>
        """, unsafe_allow_html=True)

    year_start, year_end = st.slider(
        label="", min_value=min_year, max_value=max_year, value=(2017, 2019), step=1
    )

    options = {
        "Overview": "Overview",
        "Country Analysis": "Country Analysis",
        "Product Analysis": "Product Analysis",
        "Trade Circumvention": "Trade Circumvention",
        "Policy Review": "Policy Review"
    }

    selected_label = st.radio("", list(options.keys()))
    page = options[selected_label]

    components.html("""
    <div style="text-align:center; margin-top:5px; margin-bottom:5px;">
        <div style="font-weight:700; font-size:1rem; color:#333; margin-bottom:5px;">Diyouva C. Novith</div>    
        <div style="font-size:0.95rem; color:gray; margin-top:4px; line-height:1.35;">MS. Public Policy &<br>Management,<br>Data Analytics Track</div>
        <div style="display:flex; justify-content:center; gap:18px; margin-top:12px;">
            <a href="https://www.linkedin.com/in/diyouva/" target="_blank"><img src="https://img.icons8.com/?size=100&id=13930&format=png&color=000000" width="26" height="26"></a>
            <a href="https://public.tableau.com/app/profile/diyouva.c.novith/vizzes" target="_blank"><img src="https://img.icons8.com/?size=100&id=JZIVhptAjszX&format=png&color=000000" width="26" height="26"></a>
            <a href="https://scholar.google.com/citations?user=MS7d1_kAAAAJ&hl=en" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Google_Scholar_logo.svg" width="26" height="26"></a>
        </div>
        <div style="margin-top:16px;">
            <div style="font-weight:600; font-size:0.83rem; color:#555; text-align:center;">How to Cite:</div>
            <div style="text-align:left; margin: 6px auto 0 auto; width: max-content; font-size:0.80rem; color:#777; line-height:1.3;">Novith, D. C. (2025).<br><em>US–China Trade War:<br>Detecting Trade Circumvention</em>.</div>
        </div>
        <div style="margin-top:18px; font-size:0.78rem; color:#444; text-align:center; line-height:1.35;"><strong>Final Project</strong><br>Exploratory Data Analysis &<br>Visualization with Python</div>            
    </div>
    """, height=300)

# ======================================================================
# PAGE: OVERVIEW (Combines Introduction & Methodology)
# ======================================================================
if page == "Overview":
    st.markdown('<div class="main-title">Global Trade Realignment</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">The Strategic Triangle: Assessing the Rise of ASEAN in the US-China Conflict</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class="journal-text">
        The imposition of tariffs under Section 301 of the Trade Act of 1974 marked a definitive pivot in the global economic architecture. Analyzing the period from <b>{year_start} to {year_end}</b>, this study tracks the reorganization of trans-Pacific supply chains. 
        <br><br>
        As multinational enterprises moved to diversify away from China, the Association of Southeast Asian Nations (ASEAN) emerged as the primary recipient of this manufacturing capacity. However, a critical distinction must be made between legitimate industrial expansion and trade circumvention. This study investigates whether the surge in US-ASEAN trade represents a genuine structural shift in production or a logistical mask for transshipment.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="highlight-box" style="margin-top:0px;">
        <b>Primary Inquiry:</b><br>
        Does the rise in US-ASEAN trade volume constitute a fundamental shift in production capacity, or does it indicate trade circumvention (transshipment)?
        </div>
        """, unsafe_allow_html=True)

    # --- Figure 1: Map ---
    # Filter Data for Map
    overview_df = all_df[(all_df['year'] >= year_start) & (all_df['year'] <= year_end)]
    map_df = build_intro_map_data(overview_df)
    
    # Calculate stats for dynamic text
    try:
        total_vol = map_df['Total_Trade_Billion'].sum()
        asean_vol = map_df[map_df['Group']=='ASEAN']['Total_Trade_Billion'].sum()
        chn_vol = map_df[map_df['Group']=='China']['Total_Trade_Billion'].sum()
        asean_pct = (asean_vol / total_vol) * 100 if total_vol > 0 else 0
        ratio = asean_vol / chn_vol if chn_vol > 0 else 0
    except:
        asean_pct = 0
        ratio = 0

    color_map = {'United States': '#1f77b4', 'China': '#d62728', 'ASEAN': '#2ca02c', 'Other': '#d3d3d3'}

    if not map_df.empty:
        # Only show header and chart if data exists
        # st.markdown('<div class="section-header">Figure 1: Spatial Distribution of Trade Value</div>', unsafe_allow_html=True)
        
        fig_map = px.choropleth(
            map_df, locations="iso", color="Group", hover_name="reporter",
            hover_data=["Formatted_Value"], color_discrete_map=color_map,
            projection="natural earth", title=""
        )
        fig_map.update_traces(hovertemplate="<b>%{hovertext}</b><br>Accumulated Trade: %{customdata[0]}<extra></extra>")
        fig_map.update_geos(showcountries=True, countrycolor="white", showland=True, landcolor="#f0f0f0", showocean=True, oceancolor="white", showframe=False, coastlinecolor="white")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown(f'<p class="caption-text">Figure 1. The Tri-Polar Economy ({year_start}-{year_end}). ASEAN trade volume has reached {ratio:.2f}x the size of China\'s direct volume in this dataset.</p>', unsafe_allow_html=True)

    # --- Methodology Section ---
    st.markdown("""
    <div class="journal-text">
    <b>Methodological Framework and Data Provenance</b>
    <br><br>
    To ensure rigorous detection of anomalies, this study employs bilateral trade data sourced from the UN Comtrade database via WITS, specifically restricting the product scope to high-sensitivity HS Codes targeted by Section 301 tariffs (e.g., Telecom HS 8517, Semiconductors HS 8542). 
    <br><br>
    The analytical engine relies on three core indicators. First, the <b>Mirror Share-Shift Analysis</b> quantifies the substitution effect. A perfect substitution is defined mathematically as:
    </div>
    """, unsafe_allow_html=True)

    st.latex(r'''
    \Delta S_{ASEAN} \approx - \Delta S_{China}
    ''')

    st.markdown("""
    <div class="journal-text">
    Where $S$ represents the market share of US imports. Second, the <b>Trade Intensity Index (TII)</b> measures the relative bias of ASEAN exports toward the US market. Finally, the <b>Volume Complementarity Analysis</b> tracks absolute values to verify if export surges are backed by proportional industrial capacity.
    </div>
    """, unsafe_allow_html=True)

    # --- CONCLUSION ---
    st.markdown(f"""
    <div class="highlight-box">
    <b>Strategic Synthesis: The Triangular Trade Hypothesis</b><br>
    The spatial data for the period <b>{year_start}–{year_end}</b> confirms that trade has not globalized but rather <i>regionalized</i>. The ASEAN bloc now accounts for approximately <b>{asean_pct:.1f}%</b> of the total trade volume tracked in this study. The accumulation of such significant trade volume in a region geographically contiguous to China creates a fertile environment for transshipment activities, where goods flow from China to ASEAN for re-labeling before final shipment to the US.
    </div>
    """, unsafe_allow_html=True)

# ======================================================================
# PAGE: COUNTRY ANALYSIS
# ======================================================================
elif page == "Country Analysis":
    st.markdown('<div class="main-title">Composition of US Imports</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Analyzing the Persistence of Asian Supply Chains</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="journal-text">
    The central premise of tariff policy is to encourage diversification. We test this by analyzing the aggregate composition of US imports for the targeted tariff goods between fiscal years <b>{year_start} and {year_end}</b>. If the policy were successful in broadening the supply base, we would expect a significant expansion in the "Rest of World" category relative to the Asian bloc.
    </div>
    """, unsafe_allow_html=True)

    pie_df = build_us_import_pie_data(usa_df, target_hs_list, year_start, year_end)
    
    col_pie, col_desc = st.columns([1.5, 1])

    with col_pie:
        if not pie_df.empty:
            fig_pie = px.pie(
                pie_df, values='Value', names='Source', color='Source',
                color_discrete_map={'United States': '#1f77b4','China': '#d62728','ASEAN': '#2ca02c','Rest of World': '#95a5a6'},
                hole=0.4
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown(f'<p class="caption-text">Figure 2. Proportional composition of US Imports ({year_start}-{year_end}).</p>', unsafe_allow_html=True)
        else:
            st.warning("No data available.")

    with col_desc:
        if not pie_df.empty:
            total = pie_df['Value'].sum()
            chn_val = pie_df[pie_df['Source']=='China']['Value'].sum()
            asean_val = pie_df[pie_df['Source']=='ASEAN']['Value'].sum()
            row_val = pie_df[pie_df['Source']=='Rest of World']['Value'].sum()
            
            chn_pct = chn_val/total
            asean_pct = asean_val/total
            row_pct = row_val/total
            
            st.markdown(f"""
            <div class="highlight-box" style="margin-top:0;">
            <b>Aggregate Statistics ({year_start}-{year_end})</b><br><br>
            Total Value: <b>${total/1e6:,.1f} B</b><br>
            China Share: <b>{chn_pct:.1%}</b><br>
            ASEAN Share: <b>{asean_pct:.1%}</b><br>
            Rest of World: <b>{row_pct:.1%}</b>
            </div>
            """, unsafe_allow_html=True)

            # --- DYNAMIC ANALYSIS TEXT ---
            dominance_text = "remains overwhelmingly dominant" if (chn_pct + asean_pct) > 0.5 else "shows signs of dilution"
            diversification_text = "failed to materialize" if row_pct < 0.3 else "is beginning to take hold"

    # --- CONCLUSION ---
    if not pie_df.empty:
        st.markdown(f"""
        <div class="highlight-box">
        <b>Strategic Synthesis: Sticky Supply Chains</b><br>
        The composition analysis for <b>{year_start}–{year_end}</b> reveals that the combined market share of "China + ASEAN" stands at <b>{(chn_pct+asean_pct):.1%}</b>. This indicates that the Asian supply chain {dominance_text}. 
        <br><br>
        Critically, the "Rest of World" share sits at only <b>{row_pct:.1%}</b>, suggesting that true global diversification has {diversification_text}. The data implies that supply chains have not left the region; they have simply migrated south of the Chinese border to ASEAN. This high concentration of production within a single geographic neighborhood validates the high risk of circumvention, as the industrial base remains physically contiguous.
        </div>
        """, unsafe_allow_html=True)

# ======================================================================
# PAGE: PRODUCT ANALYSIS
# ======================================================================
elif page == "Product Analysis":
    st.markdown('<div class="main-title">Product Level Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Identifying High-Risk Categories for Transshipment</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="journal-text">
    To understand the mechanics of this shift during <b>{year_start}–{year_end}</b>, we disaggregate trade flows to identify the specific product categories driving the surge. By isolating ASEAN exports to the United States, we can pinpoint which industries are moving most aggressively.
    </div>
    """, unsafe_allow_html=True)

    mask_prod = (
        (all_df['year'] >= year_start) & 
        (all_df['year'] <= year_end) & 
        (all_df['partner_iso3'] == 'USA') & 
        (all_df['flow'] == 'Export') &
        (all_df['hs4'].isin(target_hs_list))
    )
    df_prod = all_df[mask_prod]
    
    if not df_prod.empty:
        grp_cols = ['reporter', 'description'] if 'description' in df_prod.columns else ['reporter', 'hs4']
        top_exporters = df_prod.groupby(grp_cols)['value_kusd'].sum().reset_index().sort_values(by='value_kusd', ascending=False)
        top_plot = top_exporters.head(15)
        color_col = 'description' if 'description' in df_prod.columns else 'hs4'
        
        # Identify top reporter and product for dynamic text
        top_row = top_plot.iloc[0]
        top_country = top_row['reporter']
        top_product = top_row[color_col]

        fig_bar = px.bar(
            top_plot, x='value_kusd', y='reporter', color=color_col, orientation='h',
            labels={'value_kusd': 'Export Value (kUSD)', 'reporter': 'Exporting Country'}, title=""
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown(f'<p class="caption-text">Figure 3. Top ASEAN export categories to the US ({year_start}-{year_end}). {top_country} leads the volume.</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="journal-text">
        <b>Analysis of Export Composition:</b><br>
        The data for this period positions <b>{top_country}</b> as the primary alternative hub, with a massive concentration in <b>{top_product}</b>. This concentration suggests that {top_country} has successfully integrated into the value chain for this specific sector.
        <br><br>
        The sheer scale of these exports warrants scrutiny. When a single country captures such a disproportionate share of the new export volume in a short timeframe, it raises the probability that the location is being used for final assembly or transshipment rather than full-cycle manufacturing, particularly if domestic industrial investment data does not match this export velocity.
        </div>
        """, unsafe_allow_html=True)

        # --- CONCLUSION ---
        st.markdown(f"""
        <div class="highlight-box">
        <b>Strategic Synthesis: A Single Point of Failure</b><br>
        The "China Plus One" strategy is not evenly distributed; it is highly concentrated in <b>{top_country}</b> and specifically targets the <b>{top_product}</b> sector. This concentration creates a single point of failure. The dominance of these specific flows implies that US tariffs have successfully reduced direct imports from China but have inadvertently catalyzed the rapid industrialization—or the appearance thereof—of specific ASEAN neighbors in narrow product verticals.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("No export data found for the selected parameters.")

# ======================================================================
# PAGE: TRADE CIRCUMVENTION
# ======================================================================
elif page == "Trade Circumvention":
    st.markdown('<div class="main-title">Detection of Trade Circumvention</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Triangulating Statistical Anomalies</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="journal-text">
    Trade circumvention is rarely declared; it must be inferred from data anomalies. We apply a multi-factor test to detect the "Pass-Through" phenomenon during the <b>{year_start}–{year_end}</b> window: goods moving from China to ASEAN and then to the USA with minimal processing.
    </div>
    """, unsafe_allow_html=True)
    
    df_filtered = all_df[(all_df["year"] >= year_start) & (all_df["year"] <= year_end)]
    
    # 1. Share Shift
    share_df = compute_share_shift(df_filtered, target_hs_list)
    
    # Calculate correlation for dynamic text
    correlation_text = "insufficient data to determine correlation"
    if len(share_df) > 1:
        corr = share_df['china_share'].corr(share_df['asean_share'])
        if corr < -0.7:
            correlation_text = f"a strong negative correlation ({corr:.2f})"
        elif corr < -0.3:
            correlation_text = f"a moderate negative correlation ({corr:.2f})"
        else:
            correlation_text = f"a weak or positive correlation ({corr:.2f})"

    if not share_df.empty:
        fig_share = px.line(
            share_df, x="year", y=["asean_share", "china_share"],
            labels={"value": "Share of US Imports (%)", "year": "Fiscal Year"},
            color_discrete_map={"asean_share": "#2ca02c", "china_share": "#d62728"}, markers=True
        )
        new_names = {"asean_share": "ASEAN (Gaining)", "china_share": "China (Losing)"}
        fig_share.for_each_trace(lambda t: t.update(name = new_names[t.name]))
        
        # FIX: Place legend horizontally above the chart, REMOVE title
        fig_share.update_layout(legend=dict(orientation="h", y=1.1, x=0.5, xanchor='center', title_text=""))
        
        st.plotly_chart(fig_share, use_container_width=True)
        st.markdown(f'<p class="caption-text">Figure 4. The Mirror Effect: Data shows {correlation_text} between China and ASEAN market shares.</p>', unsafe_allow_html=True)

    # 2. TII & TCI
    st.markdown('<div class="journal-text"><b>Intensity and Volume Validation</b></div>', unsafe_allow_html=True)
    col_tii, col_tci = st.columns(2)
    
    top_tii_country = "N/A"
    
    with col_tii:
        tii_df = compute_tii(df_filtered, target_hs_list)
        if not tii_df.empty:
            top_reporters = tii_df.groupby('reporter')['tii'].mean().sort_values(ascending=False).head(5).index.tolist()
            top_tii_country = top_reporters[0]
            tii_plot = tii_df[tii_df['reporter'].isin(top_reporters)]
            fig_tii = px.line(tii_plot, x="year", y="tii", color="reporter", markers=True)
            
            # FIX: Place legend horizontally above the chart, REMOVE title
            fig_tii.update_layout(legend=dict(orientation="h", y=1.1, x=0.5, xanchor='center', title_text=""))
            
            st.plotly_chart(fig_tii, use_container_width=True)
            st.markdown('<p class="caption-text">Figure 5a. Trade Intensity: Export focus pivots to the US.</p>', unsafe_allow_html=True)

    with col_tci:
        tci_df = compute_tci(df_filtered, target_hs_list)
        if not tci_df.empty:
            top_reporters_tci = tci_df.groupby('reporter')['tci'].mean().sort_values(ascending=False).head(5).index.tolist()
            tci_plot = tci_df[tci_df['reporter'].isin(top_reporters_tci)]
            fig_tci = px.line(tci_plot, x="year", y="tci", color="reporter", markers=True)
            
            # FIX: Place legend horizontally above the chart, REMOVE title
            fig_tci.update_layout(legend=dict(orientation="h", y=1.1, x=0.5, xanchor='center', title_text=""))
            
            st.plotly_chart(fig_tci, use_container_width=True)
            st.markdown('<p class="caption-text">Figure 5b. Volume Surge: Validating the scale of transfer.</p>', unsafe_allow_html=True)

    # --- CONCLUSION ---
    st.markdown(f"""
    <div class="highlight-box">
    <b>Strategic Synthesis: Evidence of Pass-Through</b><br>
    The triangulation of indicators for the period <b>{year_start}–{year_end}</b> provides compelling evidence regarding trade flows. The Share-Shift analysis displays <b>{correlation_text}</b>, suggesting that US demand is simply shifting origin rather than disappearing. 
    <br><br>
    Crucially, the simultaneous spike in Trade Intensity (Fig 5a) and Volume (Fig 5b) for specific actors—most notably <b>{top_tii_country}</b>—suggests an industrial pivot that exceeds organic growth rates. This pattern is characteristic of "pass-through" trade, where the ASEAN reporter acts as a logistical bridge to bypass US tariffs on Chinese origin goods.
    </div>
    """, unsafe_allow_html=True)

# ======================================================================
# PAGE: POLICY REVIEW
# ======================================================================
elif page == "Policy Review":
    st.markdown('<div class="main-title">Policy Review & Strategic Conclusion</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">Synthesis of Findings ({year_start}–{year_end})</div>', unsafe_allow_html=True)
    
    # --- CALCULATE SUMMARY STATS FOR THE REPORT ---
    # 1. Share Shift Correlation
    df_filtered = all_df[(all_df["year"] >= year_start) & (all_df["year"] <= year_end)]
    share_df = compute_share_shift(df_filtered, target_hs_list)
    corr_val = share_df['china_share'].corr(share_df['asean_share']) if len(share_df) > 1 else 0
    
    # 2. Composition Stats
    pie_df = build_us_import_pie_data(usa_df, target_hs_list, year_start, year_end)
    if not pie_df.empty:
        total = pie_df['Value'].sum()
        asean_pct = (pie_df[pie_df['Source']=='ASEAN']['Value'].sum() / total) * 100
        chn_pct = (pie_df[pie_df['Source']=='China']['Value'].sum() / total) * 100
        row_pct = (pie_df[pie_df['Source']=='Rest of World']['Value'].sum() / total) * 100
    else:
        asean_pct = chn_pct = row_pct = 0

    st.markdown(f"""
    <div class="journal-text">
    This dashboard has systematically analyzed the reconfiguration of trans-Pacific supply chains in response to the US-China trade war during the <b>{year_start}–{year_end}</b> window. The data presents a compelling narrative of <b>regional adaptation</b> rather than global diversification.
    <br><br>
    <b>1. The Triangular Trade Reality:</b><br> 
    The "China Plus One" strategy is effective in name, but structurally, it remains deeply tethered to the Asian continent. During this period, ASEAN captured <b>{asean_pct:.1f}%</b> of the US import market for targeted goods, while the "Rest of World" held <b>{row_pct:.1f}%</b>. The proximity of ASEAN to China facilitates a high-velocity logistics channel that is indistinguishable from domestic Chinese logistics in terms of transit time.
    <br><br>
    <b>2. The Velocity of Substitution:</b><br> 
    The Share-Shift analysis reveals a correlation coefficient of <b>{corr_val:.2f}</b> between China's decline and ASEAN's rise. { "This strong negative correlation confirms a near-perfect substitution effect." if corr_val < -0.7 else "This suggests a complex decoupling process where substitution is not 1:1." } Such rapid scaling is historically unprecedented without significant pre-existing infrastructure, raising red flags for "label engineering."
    <br><br>
    <b>3. The Concentration Risk:</b><br> 
    The data consistently isolates specific ASEAN members as primary outliers. Their export profiles have become overwhelmingly correlated with US demand, creating a mono-dependency that makes them vulnerable to future regulatory scrutiny.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="highlight-box">
    <b>Final Assessment: The Limits of Tariff Policy</b><br><br>
    The empirical evidence suggests that while US tariffs successfully reduced direct bilateral deficits with China in specific HS categories, they failed to achieve the broader strategic goal of supply chain independence. The trade war has not decoupled the US from Chinese manufacturing; it has merely inserted an intermediary—ASEAN—into the value chain.
    <br><br>
    The "China -> ASEAN -> USA" circumvention route effectively neutralizes the punitive intent of Section 301 tariffs. By processing goods just enough to qualify for a new Country of Origin label, Chinese manufacturers retain access to the US market while ASEAN nations capture the logistical markup. 
    <br><br>
    <b>Recommendation:</b> Future trade policy must evolve from simple tariff barriers to comprehensive <b>Value-Added Verification</b>. Regulatory enforcement should require proof of "Substantial Transformation" within the partner country, moving beyond the superficial "Country of Origin" label. Without this structural change, the US will continue to play a game of "whack-a-mole," chasing trade deficits as they hop from one Asian neighbor to the next.
    </div>
    """, unsafe_allow_html=True)