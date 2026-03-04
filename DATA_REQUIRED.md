# Data Requirements for Forensic Audit

To maintain the high standard of accuracy required for financial and psychological forensic analysis, this project relies on two distinct classes of data: **Ground Truth (Author/Developer Claims)** and **Observed Reality (Community Data)**.

---

## 🏗️ Category 1: Ground Truth (Author/Researcher Data)

This data represents the "published rules" of the monetization system. It is used to generate the theoretical baseline for all simulations.

### **Required Specification (JSON Configs)**
When modeling a new game or event, the following data must be provided in `data/loot_configs/`:

| Field | Description | Source |
| :--- | :--- | :--- |
| `system_name` | Full name of the event/banner. | Official Game Interface |
| `base_prob` | The raw probability (0.0 to 1.0) of winning. | "Odds" or "Probabilities" button |
| `cost_per_pull_usd` | The cost of 1 single pull converted to USD. | Top-up shop conversion |
| `pity_config` | Mechanics for guaranteed items (linear or exponential). | Small print in Rules/Info |
| `acquisition_threshold` | Number of items/shards required for a full win. | Item description (e.g., 10 shards) |

### **Where to find this:**
- **In-Game "i" or "?" buttons:** Look for "Odds" or "Probability" disclosures.
- **Official Web Portals:** Most publishers (Tencent, Garena, Hoyoverse) host web-based odds pages.
- **Terms of Service:** Occasionally, pity mechanics are hidden in the ToS or "Game Rules" sections.

---

## 📊 Category 2: Observed Reality (Community Data)

This data represents actual player experiences. It is used to validate the Ground Truth and detect hidden deviations ("Silent Nerfs").

### **Required Format**
We only accept pull data in two specific formats:
1. **CSV**: Must have a header `trials_to_success`.
2. **JSON**: A flat list of integers (e.g., `[74, 8, 90, 4]`).

### **Data Quality Standards:**
- **Sample Size:** For statistical significance (95% confidence), we recommend at least **100 recorded acquisition events**.
- **Accuracy:** Data must be complete (e.g., if you recorded 500 pulls but only 2 wins, we need both numbers).
- **Verifiability:** If possible, include a link to a screenshot or recording of the pull history for audit trail purposes.

### **Where to find this:**
- **Personal Pull Logs:** Most games store 3-6 months of history.
- **Community Spreadsheets:** Search Reddit or Discord for "Pull Tracking Spreadsheets."
- **API Exporters:** Tools that extract history via the game's network requests.

---

## 🌍 Category 3: Socio-Economic Data (Author Only)

Used to translate digital costs into human labor impact.

### **Required Parameters (per region):**
- `median_daily_income_usd`: National median daily wage.
- `ppp_factor`: Purchasing Power Parity adjustment.
- `source`: A reputable source (World Bank, BLS, local labor bureaus).

### **Where to find this:**
- **World Bank Open Data:** (data.worldbank.org)
- **ILOSTAT:** International Labour Organization databases.
- **Numbeo:** For real-time cost-of-living comparisons.

---

## ✅ Verification Checklist

Before submitting data or running an analysis, verify the following:
- [ ] Does the `cost_per_pull_usd` include the cost of currency "bundles" (e.g., the $99.99 pack)?
- [ ] Is the `pity_config.start` the *exact* pull number where probability begins to increase?
- [ ] In the community data, are you counting *individual pulls* or *multi-pulls*? (We require individual counts).

**Inaccurate data leads to inaccurate warnings. Double-check your sources.**
