# Quantifying Monetization Volatility & Retention Pressure in Mobile F2P Games

## Overview
This project models mobile free-to-play (F2P) monetization as a stochastic financial architecture and behavioral retention framework. It provides a forensic toolset to quantify variance, tail concentration, and structural pressure in systems used by titles like *PUBG: Battlegrounds*, *BGMI*, and *Free Fire*.

**This is a measurement tool, not a moral platform.** We replace emotional rhetoric with distributional mathematics.

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
│   │   ├── monte_carlo.py   # Multi-stage shard/token simulation
│   │   ├── curves.py        # Pity/Soft-pity curve functions (linear/exp)
│   │   └── validator.py     # Module 0: Geometric Baseline & Chi-Squared
│   ├── metrics/
│   │   ├── risk_metrics.py  # CTE, Kurtosis, WRR
│   │   ├── retention.py     # SRI, OCA, Recovery Interest
│   │   ├── friction.py      # IG, Top-Up Pressure, LAI (Sunk Cost)
│   │   └── utility_decay.py # Meta-Relevance & Subscription Equivalence
│   ├── analysis/
│   │   ├── sensitivity.py   # Delta-Risk & Pity-Start sweeps
│   │   └── incentives.py    # Logistic regression for RIC
│   ├── utils/
│   │   ├── config_loader.py # JSON Schema validation for configs
│   │   ├── reporter.py      # Forensic reporting engine
│   │   └── community_ingestor.py # Observed data ingestion
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
uv run main.py monetization --config data/loot_configs/standard_banner.json --plot --report
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
- **Community Data Validation:** Uses **Chi-Squared Goodness-of-Fit** to compare observed community pull data (scraped from Reddit/YouTube) against simulated expectations to detect **"Silent Nerfs."**

### Module 1: Tail Risk (CTE₉₅ & WRR)
Instead of "Average Cost," we focus on **Asymmetric Variance Exposure**:
- **CTE₉₅:** Average cost for the "unlucky" 5%.
- **WRR (Whale Revenue Ratio):** $CTE_{95} / \text{Median}$. Quantifies revenue reliance on extreme outliers.
- **Utility Decay:** Translates one-time purchases into a daily **Meta-Relevance Cost**, showing the "subscription equivalent" of items that power-creep over time.
- **Forensic Reporting:** Generates human-readable Markdown reports contextualizing costs as **Days of Median Labor** across global regions.

### Module 3: Friction & Obfuscation
- **Incentive Gap (IG):** Measures forced surplus spending by comparing required costs to available currency packs.
- **Top-Up Pressure Index:** Quantifies the "residual utility" trap—the forced additional spend required to use up leftover currency balances.
- **Loss Aversion Index (LAI):** Quantifies the psychological sunk cost of **Multi-Stage Acquisition** (Shards/Tokens).
- **Bonus Obfuscation:** Quantifies the cognitive load added by "Bonus" currency math, making real-time financial assessment harder.

---

## Forensic Dashboard
The **Streamlit Forensic Dashboard** provides a high-visibility interface for:
- **Interactive CDF Analysis:** Visualize the probability of success vs. total cost.
- **Economic Pain Index:** Translate virtual costs into working days adjusted for **Purchasing Power Parity (PPP)**.
- **Multi-Stage Acquisition:** Support for shards/tokens and fragmented progression modeling.
- **Community Validation Engine:** Upload observed data to detect statistical discrepancies in published odds.
- **Psychological Pressure Simulation:** Toggle **Social Proof Bias** and **Loss Aversion** sliders to see how behavioral hacks affect perceived value.
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
