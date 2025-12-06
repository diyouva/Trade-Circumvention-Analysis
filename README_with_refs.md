# **US–China Trade War: Detecting Trade Circumvention Dashboard**
### *A Streamlit-Based Analytical Platform for Monitoring Supply Chain Shifts and Transshipment Risks*

---

## 📌 **Overview**

The **US–China Trade War: Detecting Trade Circumvention Dashboard** is an interactive Streamlit application designed to analyze potential trade circumvention behaviors triggered by Section 301 tariffs. Using bilateral trade data from **2015–2020**, the dashboard evaluates whether rising US imports from ASEAN countries indicate:

- Genuine **production relocation**, or  
- Possible **rerouting of Chinese goods** through ASEAN (transshipment)

This tool integrates economic indicators, spatial visualization, and share-shift analytics to provide a policy-relevant view of global value chain realignments. Recent research indicates that US tariffs led to substantial trade diversion toward ASEAN economies, though with mixed evidence on whether this reflects genuine industrial capacity or tariff avoidance pathways (Freund et al., 2022; Garcia-Herrero & Tan, 2023).

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
  Based on substitution dynamics documented by Fajgelbaum et al. (2020), the dashboard models how ASEAN’s rising share may statistically mirror China’s declining share.

- **📊 Trade Intensity Index (TII)**  
  Measures export bias toward the U.S. market, reflecting changes in ASEAN dependency highlighted by Kim & Lee (2023).

- **📐 Volume Complementarity Check**  
  Evaluates whether export surges are supported by realistic production capacity, consistent with global value chain restructuring literature (Antràs, 2021).

- **🧠 Dynamic Interpretation Layer**  
  Automatically updates narrative insights based on selected parameters.

### **4. Academic Presentation Style**
Designed in a scientific-journal format informed by economic policy literature.

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
│   └── USA_*.csv
│
└── assets/
    └── cmu_logo_circular.png
```

---

## 📊 **Data Sources**

- **Primary Source:**  
  United Nations Comtrade Database via World Integrated Trade Solution (WITS).

- **Scope:**  
  Bilateral trade flows focusing on HS codes affected by Section 301 tariffs, supported by tariff documentation from Bown (2020).

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
venv\Scripts\activate         # Windows
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

## 📚 **Citation (Dashboard)**

Novith, D. C. (2025). *US–China Trade War: Detecting Trade Circumvention*.

---

## 📘 **References (APA 7th Edition)**

Antràs, P. (2020). *De-globalisation? Global value chains in the post-COVID-19 world*. Economics & Statistics Working Paper.  
Bown, C. P. (2025). *US–China trade war tariffs: An up-to-date chartbook*. Peterson Institute for International Economics.  
Fajgelbaum, P. D., Goldberg, P. K., Kennedy, P. J., & Khandelwal, A. K. (2019). The return to protectionism. *The Quarterly Journal of Economics, 135*(1), 1–55.  
Freund, C., Mulabdic, A., & Piermartini, R. (2022). Is China’s trade diverting to ASEAN? *The World Bank Economic Review*.  
Garcia-Herrero, A., & Tan, X. (2023). Is ASEAN the new China? Evaluating post-tariff shifts in manufacturing. *Asian Economic Papers*.  
Kim, M., & Lee, J. W. (2023). Global value chain realignment after the US–China trade war. *Journal of Asian Economics*.  

