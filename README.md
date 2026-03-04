# Quantifying Monetization Volatility & Retention Pressure in Mobile F2P Games

## Overview
This project models mobile free-to-play (F2P) monetization as a stochastic financial architecture and behavioral retention framework. It provides a forensic toolset to quantify variance, tail concentration, and structural pressure in systems used by titles like *PUBG: Battlegrounds*, *BGMI*, and *Free Fire*.

**This is a measurement tool, not a moral platform.** We replace emotional rhetoric with distributional mathematics.

## Community & Transparency
Empower yourself with data. 

- **[COMMUNITY.md](file:///d:/opensource/F2P-Games/COMMUNITY.md):** Learn how to locate, extract, and utilize your own pull history for forensic validation.
- **[DATA_REQUIRED.md](file:///d:/opensource/F2P-Games/DATA_REQUIRED.md):** Formal specifications for Ground Truth and Observed Reality data.
- **[GLOSSARY.md](file:///d:/opensource/F2P-Games/GLOSSARY.md):** Non-technical definitions for risk metrics (CTE, WRR, SNT).

---

## System Architecture

```text
project/
├── .venv/                   # Local virtual environment managed by uv
├── data/
│   ├── loot_configs/        # JSON schemas & banner configurations
│   ├── retention_configs/   # Season length/XP requirements
│   ├── ingestion/           # Screenshot archives (for audit trails)
│   └── results/             # Simulation outputs & sensitivity plots
├── src/
│   ├── engine/
│   │   ├── monte_carlo.py   # Multi-stage & Step-Up simulation core
│   │   ├── curves.py        # Pity/Soft-pity & Step-Up curve functions
│   │   └── validator.py     # Module 0: Geometric Baseline & Chi-Squared
│   ├── metrics/
│   │   ├── risk_metrics.py  # CTE, WRR, Safety Net Tax
│   │   ├── retention.py     # SRI, OCA, Recovery Interest
│   │   ├── friction.py      # IG, Top-Up Pressure, LAI (Sunk Cost Trap)
│   │   └── utility_decay.py # Meta-Relevance & Subscription Equivalence
│   ├── analysis/
│   │   ├── sensitivity.py   # Delta-Risk & Pity-Start sweeps
│   │   └── incentives.py    # Logistic regression for RIC
│   ├── utils/
│   │   ├── config_loader.py # JSON Schema validation for configs
│   │   ├── reporter.py      # Forensic reporting engine
│   │   ├── fact_sheet.py    # Standardized PDF/A-ready export
│   │   ├── community_ingestor.py # Observed data ingestion
│   │   └── translator.py    # MBA-to-Noob translation layer
│   ├── app.py               # Streamlit Forensic Dashboard
│   ├── run_analysis.py      # CLI runner for monetization analysis
│   └── run_sensitivity.py   # CLI runner for visualization & sweeps
├── tests/                   # Verification of mathematical convergence
├── PROGRESS.md              # Detailed implementation status
├── CHANGELOG.md             # Version history
└── requirements.txt         # Project dependencies
```

---

## Getting Started

### Prerequisites
- Python 3.12+
- [astral-uv](https://github.com/astral-sh/uv) (for high-performance dependency management)

### Installation
1. Install `uv` (if not already installed):
   ```powershell
   pip install uv
   ```
2. Create virtual environment and install dependencies:
   ```powershell
   uv venv
   uv pip install -r requirements.txt
   ```

### Running Analysis
All tools should be run using `uv run` via the **Unified Runner** (`main.py`) to ensure the correct environment and error handling. Set `PYTHONPATH` to the project root.

**1. Forensic Dashboard (Recommended for Visibility)**
Launch the interactive Streamlit dashboard to visualize tail risk and labor-cost impact:
```powershell
$env:PYTHONPATH = "."; uv run main.py dashboard
```

**2. Unified Runner Entry Point**
The forensic toolset can also be controlled via `main.py` CLI:
```powershell
$env:PYTHONPATH = "."; uv run main.py --help
```

**3. Monetization Risk Analysis**
Analyze a banner's volatility and tail risk with CDF visualization and forensic reporting:
```powershell
uv run main.py monetization --config data/loot_configs/standard_banner.json --plot --report --factsheet
```

**4. State of the Tail (Big Three Comparative Audit)**
Generate a comprehensive comparative audit for PUBG, BGMI, and Free Fire:
```powershell
uv run main.py state-of-the-tail
```

**5. Friction & Obfuscation Analysis**
Quantify mental math load, including **Bonus Currency** and **Top-Up Pressure** penalties:
```powershell
uv run main.py friction --config data/loot_configs/friction_config.json
```

**5. Retention Incentive Curves (RIC)**
Model player retention response using logistic regression with standard error reporting:
```powershell
uv run main.py incentives --simulate
```

**6. Screenshot Audit Utility**
Generate a verifiable SHA256 audit trail for ingested evidence:
```powershell
uv run main.py audit
```

---

## Module Highlights

### Module 0: Integrity & Investigation
- **Geometric Baseline:** Validates that static probability simulations converge to $E[N] = 1/p$ within <0.5% deviation.
- **Step-Up Support:** Engine handles variable costs and probabilities per trial, modeling the "Step-Up Trap" where costs inflate as acquisition nears.
- **Secondary Logic (Genshin/Weapon):** Engine handles complex guarantees like the "50/50" flip and "Epitomized Path" logic (multi-failure guarantees).
- **Exhaustive Mode (CODM):** Specialized **Hypergeometric simulation** for Lucky Draws where items are removed from the pool, causing costs to escalate.
- **Community Data Validation:** Uses **Chi-Squared Goodness-of-Fit** to compare observed community pull data (scraped from Reddit/YouTube) against simulated expectations to detect **"Silent Nerfs."**

### Module 1: Tail Risk (CTE₉₅ & WRR)
Instead of "Average Cost," we focus on **Asymmetric Variance Exposure**:
- **CTE₉₅ (The Nightmare Scenario):** Average cost for the "unlucky" 5%.
- **WRR (The Unlucky Tax):** $CTE_{95} / \text{Median}$. Quantifies revenue reliance on extreme outliers.
- **Safety Net Tax (The Hidden Pity Cost):** Quantifies the premium players pay for the variance protection of pity systems.
- **Transparency Trap (Sensitivity Sweep):** Automated audit for systems with undisclosed or ultra-low rates to show how tail risk explodes without transparency.
- **Utility Decay:** Translates one-time purchases into a daily **Meta-Relevance Cost**, showing the "subscription equivalent" of items that power-creep over time.
- **Forensic Reporting:** Generates human-readable Markdown reports and **Standardized Fact Sheets** contextualizing costs using **Grocery Math**, **Months of Rent**, and **Big Mac Equivalents** across global regions.

### Module 3: Friction & Obfuscation
- **Incentive Gap (IG):** Measures forced surplus spending by comparing required costs to available currency packs.
- **Top-Up Pressure Index:** Quantifies the "residual utility" trap—the forced additional spend required to use up leftover currency balances.
- **The Sunk Cost Trap (LAI):** Quantifies the psychological sunk cost of **Multi-Stage Acquisition** (Shards/Tokens) with visceral warnings.
- **Bonus Obfuscation:** Quantifies the cognitive load added by "Bonus" currency math, making real-time financial assessment harder.

---

## Forensic Dashboard
The **Streamlit Forensic Dashboard** provides a high-visibility interface for:
- **Plain-English Verdicts**: Uses the MBA-to-Noob translation layer to immediately summarize predatory design or fair pricing at a glance.
- **Interactive CDF Analysis (The Money Pit):** Visualize "The Coin Flip", "The Guarantee", and the shaded variance trap.
- **Economic Pain Index & Life Clock:** Translate virtual costs into **Weeks of Groceries**, **Months of Rent**, and working days adjusted for **PPP**.
- **Seasonal Portfolio Sim:** Quantify the probability of being unlucky across multiple banners in a single season.
- **Transparency Grading:** Instant A-F grade with human-centric subtitles for every banner.
- **Transparency Trap Analysis:** Automated sensitivity sweep to expose the cost of undisclosed odds.
- **Multi-Stage & Step-Up Acquisition:** Support for shards/tokens and variable trial costs/probabilities.
- **Community Validation Engine:** Upload observed data to detect statistical discrepancies in published odds.
- **Forensic Documentation:** Generate and download **Standardized Fact Sheets** directly from the UI.
- **Psychological Pressure Simulation:** Toggle **Social Proof Bias** and **Sunk Cost Trap** sliders to see how behavioral hacks affect perceived value.
- **State of the Tail Comparative Audit:** Side-by-side comparison of major F2P titles.

---

## Contributing Configs
Help build the **Forensic Registry of Loot Box Risks**. We encourage contributions of banner configurations from different games and regions.

### How to Submit:
1.  Review the `data/loot_configs/loot_schema.json` for requirements.
2.  Create a new JSON file in `data/contributions/` following the schema.
3.  Include a screenshot of the published rates in `data/ingestion/` for verification.
4.  Submit a Pull Request with your new configuration.

---

## Implementation Standards
- **Vectorization:** Simulation core uses `NumPy` vectorized operations for high performance.
- **Reproducibility:** All runs use a fixed PRNG `seed`.
- **Validation:** JSON Schema validation ensures configuration integrity.

---

### Project Philosophy
Mobile monetization is not a mystery; it is a solved mathematical problem. This repository exists to make those solutions transparent. **Measure twice. Claim once.**
