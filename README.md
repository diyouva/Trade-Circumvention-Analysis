US-China Trade War: Detecting Trade Circumvention Dashboard

This project is a Streamlit-based interactive dashboard designed to analyze and visualize the potential trade circumvention occurring as a result of the US-China trade war. It focuses on the shift in supply chains towards ASEAN countries and uses various economic indicators to detect transshipment activities.

Overview

The dashboard provides a comprehensive analysis of trade data from 2015 to 2020, specifically targeting high-sensitivity HS codes affected by Section 301 tariffs. It aims to answer whether the increased US-ASEAN trade is due to legitimate production shifts or if it masks the rerouting of Chinese goods.

Features

Interactive Period Filter: Analyze data across different timeframes (2015-2020).

Scientific Visualization:

Overview Map: A spatial distribution map highlighting the trade volume of major economic blocs (US, China, ASEAN).

Composition Analysis: Donut charts showing the share of US imports from China, ASEAN, and the Rest of the World.

Product Level Drill-down: Bar charts identifying top ASEAN exporters and specific product categories (e.g., Electronics, Furniture) driving the trade surge.

Circumvention Detection:

Mirror Share-Shift Analysis: Visualizing the correlation between the decline in China's market share and the rise in ASEAN's share.

Trade Intensity Index (TII): Measuring the export focus of ASEAN nations towards the US.

Volume Complementarity: Tracking the absolute volume of exports to validate industrial capacity.

Dynamic Analysis & Synthesis: All conclusions and strategic syntheses automatically update based on the selected time period and underlying data.

Scientific Journal Style: The dashboard is presented with a formal academic tone, suitable for policy review and economic analysis.

Project Structure

/root
  ├── streamlit.py          # Main application file
  ├── styles.css            # Custom CSS for styling
  ├── requirements.txt      # Python dependencies
  ├── README.md             # Project documentation
  ├── modules/              # Custom Python modules
  │   ├── data_load2.py     # Data loading and cleaning functions
  │   └── utils2.py         # Calculation logic for trade indices
  ├── data/                 # Data folder (contains CSV files)
  │   ├── ASEAN_*.csv
  │   ├── China_*.csv
  │   └── USA_*.csv
  └── assets/               # Static assets (images)
      └── cmu_logo_circular.png


Data Sources

Source: United Nations Comtrade Database via World Integrated Trade Solution (WITS).

Scope: Bilateral trade flows for HS codes targeted by Section 301 tariffs (e.g., HS 8517, 8542, 8471, 9401).

Installation & Usage

Clone the repository:

git clone <repository_url>
cd <project_directory>


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run the application:

streamlit run streamlit.py


Author

Diyouva C. Novith

MS. Public Policy & Management, Data Analytics Track

Final Project - Exploratory Data Analysis & Visualization with Python

Citation

Novith, D. C. (2025). US–China Trade War: Detecting Trade Circumvention.