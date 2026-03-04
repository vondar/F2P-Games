# Community Forensic Data Guide

Welcome to the **F2P Forensic Audit Platform**. This guide empowers players and community researchers to bridge the gap between "published odds" and "actual outcomes." 

By contributing your data, you help the community detect "Silent Nerfs," validate pity systems, and quantify the true cost of digital items.

---

## 🔍 Locating Your Data

Most modern F2P games (especially those operating in regions like China, Japan, or the EU) are required to provide a **Pull History** or **Transaction Log**.

### Common Locations:
- **PUBG Mobile / BGMI:** Settings -> Customer Service -> Records -> Crate/Spin History.
- **Genshin Impact / Honkai: Star Rail:** Feedback -> Record -> Wish/Warp History.
- **Free Fire:** Vault -> History (or external web-based history portal).

### How to Extract:
1. **Manual Entry:** For small samples (e.g., your last 50 pulls), record the number of pulls it took to get the "Grand Prize" or "Legendary Item."
2. **Community Trackers:** Use trusted third-party tools (like *Paimon.moe* for Genshin or *Star Rail Station*) that export your history to CSV or JSON.
3. **Network Sniffing (Advanced):** Tools like Fiddler or specialized "history exporters" can capture the data directly from the game's API responses.

---

## 📤 Accessing & Utilizing Data in the Project

The Forensic Audit Platform supports two primary ways to use your data:

### 1. The Interactive Dashboard (Recommended)
Launch the dashboard to visualize your data against the mathematical ideal:
```powershell
streamlit run src/app.py
```
- **Navigate to:** "Community Validation" section.
- **Upload:** Drag and drop your `.csv` or `.json` file.
- **Compare:** The dashboard will run a **Chi-Squared Goodness-of-Fit** test to see if your luck matches the developer's claims.

### 2. The Forensic Engine (CLI)
For researchers performing bulk analysis, use the ingestion scripts:
```powershell
python src/run_analysis.py --input data/my_observed_data.csv
```

---

## 🛠️ Data Formats

To ensure the engine can read your data, use one of the following formats:

### **Option A: CSV (Recommended)**
A single column named `trials_to_success` representing how many pulls it took for each acquisition.
```csv
trials_to_success
14
82
7
55
```

### **Option B: JSON**
A simple list of integers representing the pull counts.
```json
[14, 82, 7, 55]
```

---

## 🛡️ Privacy & Security

- **No Personal Identifiers:** This project **never** asks for your Player ID, Username, or Password.
- **Local Processing:** All analysis happens on **your machine**. We do not upload your raw data to any server.
- **Anonymization:** If you contribute data to the project's `data/results/` folder for others to see, ensure you have removed any metadata that could identify your account.

---

## ❓ Troubleshooting

- **"File not recognized":** Ensure your CSV has the header `trials_to_success`.
- **"Statistical Discrepancy":** If the engine returns "DISCREPANCY DETECTED," it doesn't always mean the game is rigged. Small sample sizes (less than 100 successes) can lead to false positives.
- **"Zero Counts":** If you have zero successes in your data, the engine cannot perform a Chi-Squared test. You need at least one acquisition event.

---

## 🤝 How to Contribute

Found a new crate or event? 
1. Create a new JSON config in `data/loot_configs/`.
2. Model the pity system using the `loot_schema.json` rules.
3. Submit a Pull Request to help the community audit the new content.

**Together, we make the math impossible to ignore.**
