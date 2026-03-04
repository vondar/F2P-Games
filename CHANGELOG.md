# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-04

### Added
- **Dashboard Sidebar Overhaul**: Reorganized the Streamlit sidebar into a "Three-Tier" structure (Selection, Presets, Scenarios) and hid advanced inputs inside an "Advanced Forensic Lab" expander.
- **MBA-to-Noob Translation Layer**: Translated technical metrics into plain English (e.g., "95% Confidence Budget" -> "The 'Safe' Budget", "WRR" -> "The Unlucky Tax") via `src/utils/translator.py`.
- **Luck-o-Meter**: Added gauge charts for WRR and SNT to provide a visual hierarchy of fairness.
- **Annotated Confidence Curve**: Enhanced CDF plot with marked "The Coin Flip" and "The Guarantee" points, highlighting "The Money Pit" variance trap.
- **Grocery Math & Life Clock**: Contextualized labor costs using "Weeks of Groceries" and "Months of Rent" equivalents, with a 1-year progress bar visual.
- **Sunk Cost Trap**: Renamed Loss Aversion Index (LAI) in the UI and added a visceral warning mechanic for players deep into partial progress.
- **Forensic Summary Box**: Added a plain-English "Verdict" box summarizing the banner's risk profile at the top of the dashboard.

## [0.1.0] - 2026-03-02

### Added
- Initial project structure based on architecture defined in README.
- Directories for engine, metrics, analysis, data, and tests.
- PROGRESS.md for tracking implementation details.
- CHANGELOG.md for versioning.
- Core engine modules: `monte_carlo.py`, `curves.py`, `validator.py`.
- Metrics modules: `risk_metrics.py`, `retention.py`, `friction.py`.
- Analysis modules: `sensitivity.py`, `incentives.py`.
- Data schemas and configuration templates for loot systems.
- Initial test suite for engine convergence validation.
- Integration with `astral-uv` for dependency management and execution.

## [0.2.0] - 2026-03-02

### Added
- JSON Schema validation for loot configurations.
- Support for exponential soft-pity curves in addition to linear ones.
- `run_analysis.py` CLI tool for end-to-end simulation and risk assessment.
- `run_sensitivity.py` for visualizing the financial impact of pity trigger shifts.
- Comprehensive unit test suite for risk, retention, and friction metrics in `tests/test_metrics.py`.
- `run_retention.py` for analyzing digital debt and schedule rigidity.
- `src/utils/audit.py` for SHA256 screenshot verification and audit trails.
- Logistic regression implementation for Retention Incentive Curves (RIC) in `src/analysis/incentives.py`.

## [0.3.0] - 2026-03-02

### Added
- `run_friction.py` for analyzing pack size gaps and currency obfuscation.
- `run_incentives.py` for performing RIC analysis on player data.
- CDF visualization in `run_analysis.py` for "Confidence Budget" transparency.
- `main.py` as a unified entry point for all modules.
- New configurations for friction and Battle Pass analysis.

## [0.4.0] - 2026-03-02

### Added
- Standard Error reporting for logistic coefficients in RIC analysis.
- Significance testing for retention-incentive correlations.
- `Bonus Obfuscation Penalty` for friction metrics to model "mental math" load.
- Real-world piecewise curve model for PUBG-style crates in `data/loot_configs/pubg_crate_example.json`.
- Comprehensive error reporting and stack trace preservation in `main.py`.
- Module 0 Calibration config for 1% static drop validation.

## [0.5.0] - 2026-03-02

### Added
- "State of the Tail" comparative audit for the Big Three mobile F2P titles (PUBG, BGMI, Free Fire).
- Automated forensic reporting engine (`src/utils/reporter.py`) generating human-readable Markdown summaries.
- Labor-cost contextualization using `data/geo_configs.json` to translate virtual costs into real-world labor days.
- Real-world loot configurations for major F2P titles in `data/loot_configs/`.
- `state-of-the-tail` command in the unified runner (`main.py`).

### Fixed
- Normalization of cross-game costs by implementing USD-based labor metrics.
- Configuration drift in cross-game audits by using centralized geo-configs.

### Fixed
- "Ghosting" in incentive analysis where noisy data could lead to false significance.
- Swallow of error details in the unified runner during module failures.

### Fixed
- Improved convergence for logistic curve fitting in incentive analysis.
- Better error handling in retention debt calculations for impossible recovery scenarios.

### Fixed
- Vectorized indexing bug in Monte Carlo engine where trials were incorrectly mapped to active simulations.
- PowerShell compatibility issues for directory creation and environment variable setting.
- Division-by-zero risk in retention recovery debt calculations.

## [0.6.0] - 2026-03-02

### Added
- **Streamlit Forensic Dashboard**: A high-visibility interactive UI for quantifying monetization risk.
- **Labor Cost Contextualizer**: Visualizing acquisition costs in terms of working days (Median vs. Minimum Wage) for global regions.
- **Top-Up Pressure Index**: New metric in `friction.py` to quantify the forced additional spend required by residual currency.
- Support for launching the dashboard via `main.py dashboard`.
- Enhanced `geo_configs.json` with Minimum Wage data points.

## [1.0.0] - 2026-03-04

### Added
- **Secondary Logic Support**: Engine now handles conditional guarantees like the Genshin "50/50" flip.
- **Epitomized Path Logic**: Specialized multi-failure guarantee tracking for weapon banners.
- **Exhaustive Mode**: Support for Hypergeometric simulations (CODM Lucky Draws) with escalating costs.
- **Transparency Grading (A-F)**: Automated banner scoring based on WRR, SNT, and obfuscation metrics.
- **Transparency Trap (Sensitivity Sweep)**: Automated analysis of undisclosed rate impact on confidence budgets.
- **Big Mac Index Integration**: New economic metric to contextualize global acquisition costs.
- **COMMUNITY.md & DATA_REQUIRED.md**: Comprehensive documentation for community data discovery and contribution.
- **Multi-Stage Sunk Cost Anchor**: Forensic identification of "locked-in" upgrade paths in reports.
- **Initial Discount Support**: Support for trial-specific cost overrides (e.g., first-spin discounts).

### Fixed
- Vectorized probability resolution in `monte_carlo.py` for per-iteration pity counters.
- Fixed `AxisError` in `run_analysis.py` for 0-dim array indexing.
- Fixed Streamlit slider type-safety for probability inputs.
- Mandatory `cost_per_pull_usd` validation in `config_loader.py`.

## [0.9.0] - 2026-03-02

### Added
- **Step-Up Sequence Support**: Engine now handles variable costs and probabilities per trial, modeling the "Step-Up Trap."
- **Standardized Forensic Fact Sheet**: Automated generation of Markdown/PDF-ready reports for consumer protection.
- **Safety Net Tax (SNT)**: New metric to quantify how much players pay for the variance protection of pity systems.
- **Fact Sheet Download**: Integrated report generation and download button in the Dashboard.
- **Acquisition Cost Tracking**: Monte Carlo engine now returns total USD cost per iteration, accounting for step-up inflation.

### Fixed
- Backward compatibility for `calculate_risk_metrics` to support both legacy and v0.9.0 data formats.
- Corrected audit trail linking in generated fact sheets.

## [1.0.0] - 2026-03-02

### Added
- **Seasonal Portfolio Simulator**: Quantifies "Seasonal Tail Coincidence" and the probability of hitting multiple financial "Black Swans" in one season.
- **Transparency Score (A-F)**: A single, non-technical grade for loot banners based on WRR, SNT, and Obfuscation metrics.
- **Forensic Sanity Checks**: Robust config validation to prevent nonsensical simulation parameters (zero probability, negative costs).
- **GLOSSARY.md**: Comprehensive guide for non-technical users (journalists, regulators).
- **PPP-Adjusted Labor Data**: Updated 2026 economic data for global regions.
- **Anti-Forensic Detection (Rate Drift)**: Dashboard utility to test the sensitivity of community data against dynamic rate shifting.

### Fixed
- Dependency lockdown in `requirements.txt` for v1.0 stability.
- Improved error handling for nonsensical architectures in `config_loader.py`.

### Fixed
- Dependencies updated to include `streamlit` and `plotly` for visualization.

## [0.7.0] - 2026-03-02

### Added
- **Multi-Stage Acquisition Engine**: `monte_carlo.py` now supports shards/tokens with configurable acquisition thresholds.
- **Utility Decay Metric**: New module `utility_decay.py` to calculate the "Subscription Equivalent" of one-time purchases based on meta-relevance.
- **Social Proof Bias Simulation**: Dashboard toggle to visualize perceived vs. actual probability based on behavioral heuristics.
- **Acquisition Threshold UI**: Added shard/token control to the Streamlit sidebar.
- **Contribution Framework**:- Formalize `data/contributions/` registry and submission guide in `README.md`.

## [0.8.0] - 2026-03-02

### Added
- **Community Validation Engine**: Support for uploading observed community pull data (CSV/JSON).
- **Chi-Squared Goodness-of-Fit Test**: Statistical comparison between simulated expectations and community observations to detect "Silent Nerfs."
- **Loss Aversion Index (LAI)**: New metric in `friction.py` to quantify the psychological sunk cost of partial progress.
- **PPP-Adjusted Labor Costs**: Enhanced geo-configs with Purchasing Power Parity to reflect true economic pain.
- **Raw Data View**: Dashboard toggle to inspect descriptive statistics of the simulation results.
- **Community Ingestor**: Utility module for handling external data formats.

### Fixed
- Improved `validator.py` with scipy-based statistical testing.
- Enhanced socio-economic accuracy in labor-cost visualizations.

### Fixed
- Updated `reporter.py` to include Utility Decay analysis in all forensic summaries.
- Standardized `run_analysis.py` parameters to support multi-stage threshold overrides.
