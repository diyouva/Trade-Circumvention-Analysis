# **US–China Trade War: Detecting Trade Circumvention Dashboard**
### *A Streamlit-Based Analytical Platform for Monitoring Supply Chain Shifts and Transshipment Risks*

---

## 📌 **Overview**

The **US–China Trade War: Detecting Trade Circumvention Dashboard** is an interactive Streamlit application designed to analyze potential trade circumvention behaviors triggered by Section 301 tariffs. Using bilateral trade data from **2015–2020**, the dashboard evaluates whether rising US imports from ASEAN countries indicate:

- Genuine **production relocation**, or  
- Possible **rerouting of Chinese goods** through ASEAN (transshipment)

This tool integrates economic indicators, spatial visualization, and share-shift analytics to provide a policy-relevant view of global value chain realignments.

---

## 🔍 **Key Features**

### **1. Interactive Time Exploration**
Analyze trade behavior dynamically across selected periods (2015–2020).

### **2. Scientific Visualization Suite**
- **🌍 Overview Map**  
  Spatial distribution of trade values across US, China, and ASEAN (others shown in grey).

- **🍩 Composition Analysis**  
  Donut/pie charts revealing the proportion of US imports sourced from China, ASEAN, and the Rest of the World.

- **📦 Product-Level Drill-Down**  
  Identify top ASEAN exporters and high-sensitivity HS categories (e.g., 8517, 8471, 8542, 9401).

### **3. Circumvention Detection Framework**
- **📉→📈 Mirror Share-Shift Analysis**  
  Visual correlation between China’s declining market share and ASEAN’s corresponding rise.

- **📊 Trade Intensity Index (TII)**  
  Measures how concentrated a country’s exports are toward the US market.

- **📐 Volume Complementarity Check**  
  Validates whether export increases align with realistic industrial capacity.

- **🧠 Dynamic Interpretation Layer**  
  Narrative conclusions automatically update based on user selections and transformed datasets.

### **4. Academic Presentation Style**
Designed in a scientific-journal aesthetic suitable for policy reviews, research dissemination, and conference presentations.

---

## 📂 **Project Structure**

```
/root
├── streamlit.py            # Main Streamlit application
├── styles.css              # Custom journal-style CSS
├── requirements.txt        # Python dependencies list
├── README.md               # Project documentation
│
├── modules/
│   ├── data_load2.py       # Data ingestion & cleaning functions
│   └── utils2.py           # Computation of indices (TII, share-shift, etc.)
│
├── data/                   # UN Comtrade / WITS datasets
│   ├── ASEAN_*.csv
│   ├── China_*.csv
│   ├── HS4 Trade War US China.csv
│   └── USA_*.csv
│
└── assets/
    └── cmu_logo_circular.png
```

---

## 📊 **Data Sources**

- **Primary Source:**  
  *United Nations Comtrade Database* via **World Integrated Trade Solution (WITS)**.

- **Scope:**  
  Bilateral trade flows focusing on HS codes impacted by Section 301 tariffs, including (but not limited to):  
  **HS 8517, 8471, 8542, 9401**.

---

## ⚙️ **Installation & Usage**

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd <project_directory>
```

### **2. (Optional) Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# or
venv\Scripts\activate           # Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Launch the Streamlit Dashboard**
```bash
streamlit run streamlit.py
```

---

## 👨‍💻 **Author**

**Diyouva C. Novith**  
*M.S. Public Policy & Management — Data Analytics Track*  
Final Project for **Exploratory Data Analysis & Visualization with Python**

---

## 📚 **Citation**

If you reference or build upon this project, please cite:

> **Novith, D. C. (2025). *US–China Trade War: Detecting Trade Circumvention*.**
