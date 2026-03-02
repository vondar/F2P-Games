import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from src.engine.monte_carlo import run_monte_carlo_sim
from src.engine.validator import perform_chi_squared_test
from src.metrics.risk_metrics import calculate_risk_metrics
from src.metrics.friction import calculate_loss_aversion_index
from src.utils.config_loader import load_loot_config
from src.utils.community_ingestor import ingest_community_data, calculate_distribution_counts
from src.analysis.seasonal_sim import simulate_seasonal_load
from src.utils.fact_sheet import generate_fact_sheet
from src.utils.reporter import generate_forensic_summary

st.set_page_config(page_title="F2P Forensic Dashboard", layout="wide")

st.title("📊 F2P Forensic Dashboard: Quantifying Monetization Risk")
st.markdown("""
This dashboard visualizes the **Tail Risk** and **Socio-Economic Impact** of mobile F2P loot systems.
It moves beyond 'Average Cost' to show the real price paid by the unluckiest players.
""")

# --- Sidebar: Configuration ---
st.sidebar.header("System Configuration")

# Load available configs
config_dir = "data/loot_configs/"
available_configs = [f for f in os.listdir(config_dir) if f.endswith(".json") and f != "loot_schema.json"]
selected_config_file = st.sidebar.selectbox("Select Banner Config", available_configs)

# Load geo configs
with open("data/geo_configs.json", "r") as f:
    geo_data = json.load(f)

# --- Community Validation Data ---
st.sidebar.divider()
st.sidebar.header("Community Validation")
uploaded_file = st.sidebar.file_uploader("Upload Observed Pull Data (CSV/JSON)", type=['csv', 'json'])

# --- Simulation & Core Metrics ---
config = load_loot_config(os.path.join(config_dir, selected_config_file))

base_prob = st.sidebar.slider("Base Probability", 0.001, 0.05, config.get("base_prob", 0.01), format="%.3f")
threshold = st.sidebar.number_input("Acquisition Threshold (Shards)", min_value=1, value=config.get("acquisition_threshold", 1))
iterations = st.sidebar.select_slider("Iterations", options=[10000, 50000, 100000], value=50000)
cost_per_pull = st.sidebar.number_input("Cost per Pull ($)", value=config.get("cost_per_pull_usd", 1.0))

social_proof = st.sidebar.toggle("Enable Social Proof Bias", help="Simulate perceived probability based on frequent global win announcements.")
rate_drift = st.sidebar.toggle("Simulate Rate Drift (Anti-Forensic)", help="Simulate a scenario where p drops by 20% after 50 trials to test Chi-Squared sensitivity.")
show_raw_data = st.sidebar.checkbox("Show Raw Data", value=False)

if st.sidebar.button("Run Forensic Analysis"):
    with st.spinner("Running Monte Carlo Simulations..."):
        # Apply Rate Drift if active
        effective_pity = config.get("pity_config")
        if rate_drift:
            # Inject a 'drift' where p drops after 50 trials
            effective_pity = effective_pity.copy() if effective_pity else {"type": "linear", "start": 100, "end": 100}
            effective_pity["step_up"] = {"50": base_prob * 0.8} # 20% drop at trial 50
            st.warning("🕵️ **Rate Drift Active:** Success probability will drop by 20% at trial 50.")

        sim_data = run_monte_carlo_sim(
            base_prob=base_prob,
            iterations=iterations,
            pity_config=config.get("pity_config"),
            seed=42,
            acquisition_threshold=threshold
        )
        
        # Social Proof Simulation
        if social_proof:
            st.warning("📣 **Social Proof Bias Active:** Visualizing perceived vs. actual probability.")
            # Heuristic: Seeing 10 wins/min makes p feel 5x higher to the human brain
            perceived_p = min(0.99, base_prob * 5)
            st.info(f"Actual Odds: {base_prob:.2%} | **Perceived Odds (Bias): {perceived_p:.2%}**")
            
        metrics = calculate_risk_metrics(sim_data)
        
        # --- Layout: Transparency Grade ---
        st.divider()
        grade_color = "green" if metrics['transparency_grade'] in ['A', 'B'] else "orange" if metrics['transparency_grade'] == 'C' else "red"
        st.markdown(f"<h2 style='text-align: center;'>Transparency Grade: <span style='color: {grade_color};'>{metrics['transparency_grade']}</span></h2>", unsafe_allow_html=True)
        st.progress(metrics['transparency_score'] / 100.0)
        
        # --- Layout: Key Forensic Metrics ---
        col1, col2, col3, col4 = st.columns(4)
        
        median_cost = metrics['median_cost']
        p95_cost = metrics['p95_cost']
        cte95_cost = metrics['cte95_cost']
        wrr = metrics['wrr']
        
        col1.metric("Median Cost", f"${median_cost:,.2f}")
        col2.metric("95% Confidence Budget", f"${p95_cost:,.2f}", 
                   delta=f"{(p95_cost/median_cost - 1)*100:.1f}% vs Median", delta_color="inverse")
        col3.metric("Unlucky 5% Cost (CTE₉₅)", f"${cte95_cost:,.2f}")
        col4.metric("Whale Revenue Ratio (WRR)", f"{wrr:.2f}x", 
                   help="Quantifies how much more the tail-end outliers pay compared to the median player.")

        # --- Psychology: Loss Aversion Index ---
        st.subheader("🧠 Psychological Pressure: Loss Aversion Index (LAI)")
        # Simulate a user halfway through acquisition
        current_shards = st.slider("Simulate Current Progress (Shards)", 0, int(threshold), int(threshold * 0.8))
        lai_metrics = calculate_loss_aversion_index(current_shards, threshold, cost_per_pull)
        
        col_lai1, col_lai2, col_lai3 = st.columns(3)
        col_lai1.metric("Completion Ratio", f"{lai_metrics['completion_ratio']:.1%}")
        col_lai2.metric("Perceived Value Multiplier", f"{lai_metrics['perceived_value_multiplier']:.2f}x",
                       help="How much more valuable the next shard feels compared to the first one.")
        col_lai3.metric("Abandonment Penalty", f"${lai_metrics['abandonment_penalty_usd']:,.2f}",
                       help="The financial value of progress forfeited if the player stops now.")
        
        st.info(f"💡 **The Sunk Cost Trap:** At {lai_metrics['completion_ratio']:.1%}, the next pull is psychologically worth **{lai_metrics['perceived_value_multiplier']:.2f}x** its mathematical value.")

        # --- Community Validation Section ---
        if uploaded_file:
            st.divider()
            st.subheader("🕵️ Community Data Validation (Goodness-of-Fit)")
            
            # Save file temporarily to ingest
            temp_path = f"data/results/temp_upload_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            obs_data = ingest_community_data(temp_path)
            
            if isinstance(obs_data, dict) and "error" in obs_data:
                st.error(f"Ingestion Error: {obs_data['error']}")
            else:
                # Calculate counts for test
                obs_counts, bins = calculate_distribution_counts(obs_data)
                exp_counts, _ = calculate_distribution_counts(sim_data["trials"], bins=bins)
                
                chi_results = perform_chi_squared_test(obs_counts, exp_counts)
                
                if chi_results["is_statistically_significant"]:
                    st.error(f"🚨 **{chi_results['verdict']}** (p-value: {chi_results['p_value']:.4f})")
                    st.markdown("""
                    **The community data does NOT match the simulated model.** This suggests either:
                    1.  **Silent Nerfs:** The actual drop rates are lower than published.
                    2.  **Sampling Bias:** The uploaded data is not a representative sample.
                    """)
                else:
                    st.success(f"✅ **{chi_results['verdict']}** (p-value: {chi_results['p_value']:.4f})")
                    st.markdown("The observed community data is statistically consistent with the published model.")

        # --- Visualization: Tail Risk CDF ---
        st.subheader("📈 The 'Confidence Budget' Curve")
        x_sorted = np.sort(sim_data["costs"])
        y_cdf = np.arange(len(x_sorted)) / float(len(x_sorted))
        
        fig_cdf = px.line(x=x_sorted, y=y_cdf, labels={'x': 'Total Cost ($)', 'y': 'Probability of Success'})
        fig_cdf.add_vline(x=median_cost, line_dash="dash", line_color="gray", annotation_text=f"Median: ${median_cost:,.0f}")
        fig_cdf.add_vline(x=p95_cost, line_dash="dash", line_color="red", annotation_text=f"95% Confidence: ${p95_cost:,.0f}")
        st.plotly_chart(fig_cdf, use_container_width=True)

        # --- Socio-Economic Context: Labor Cost Calculator ---
        st.subheader("🛠️ Global Labor Cost Contextualizer (PPP Adjusted)")
        st.markdown(f"How many days of labor does a **95% Confidence Budget (${p95_cost:,.2f})** represent?")
        
        chart_data = []
        for region, data in geo_data["regions"].items():
            ppp = data.get("ppp_factor", 1.0)
            # Pain index: Adjusted days labor * PPP factor
            chart_data.append({"Region": region, "Days": (p95_cost / data["median_daily_income_usd"]) / ppp, "Type": "Median Wage (PPP Adj)"})
            chart_data.append({"Region": region, "Days": (p95_cost / data["minimum_daily_income_usd"]) / ppp, "Type": "Min Wage (PPP Adj)"})
        
        df_chart = pd.DataFrame(chart_data)
        
        fig_labor = px.bar(df_chart, x="Region", y="Days", color="Type", barmode="group",
                          title="Economic Pain Index: Labor Days Adjusted for Purchasing Power",
                          labels={"Days": "Working Days (Pain Adjusted)"})
        st.plotly_chart(fig_labor, use_container_width=True)

        st.divider()
        st.subheader("📑 Forensic Documentation")
        if st.button("Generate Standardized Fact Sheet"):
            results = {"metrics": metrics, "sim_data": sim_data, "config": config}
            system_name = selected_config_file.replace(".json", "")
            report_content = generate_forensic_summary(results, geo_data)
            fact_sheet_path = os.path.join("data/results/", f"fact_sheet_{system_name.replace(' ', '_')}.md")
            generate_fact_sheet(results, report_content, fact_sheet_path)
            st.success(f"Standardized Fact Sheet generated at {fact_sheet_path}")
            with open(fact_sheet_path, "r") as f:
                st.download_button("Download Fact Sheet (Markdown)", f, file_name=f"fact_sheet_{system_name}.md")

        if show_raw_data:
            st.divider()
            st.subheader("📄 Raw Forensic Data")
            st.dataframe(pd.DataFrame({
                "Trial Count": sim_data["trials"],
                "Estimated Cost ($)": sim_data["costs"]
            }).describe())
else:
    st.info("Select a configuration in the sidebar and click 'Run Forensic Analysis' to begin.")

st.sidebar.divider()
st.sidebar.header("Seasonal Portfolio Sim")
if st.sidebar.button("Simulate Seasonal Load"):
    st.divider()
    st.header("🌩️ Seasonal Portfolio Risk: The 'Black Swan' Analysis")
    
    # Use the 'Big Three' for the seasonal simulation
    configs = [
        load_loot_config("data/loot_configs/pubg_premium_crate.json"),
        load_loot_config("data/loot_configs/bgmi_mythic_spin.json"),
        load_loot_config("data/loot_configs/free_fire_diamond_royale.json")
    ]
    
    with st.spinner("Simulating 50,000 Seasonal Life-Cycles..."):
        seasonal_res = simulate_seasonal_load(configs, iterations=50000)
        
        col_s1, col_col_s2, col_s3 = st.columns(3)
        col_s1.metric("Median Seasonal Cost", f"${seasonal_res['median_seasonal_cost']:,.2f}")
        col_col_s2.metric("95% Seasonal Budget", f"${seasonal_res['p95_seasonal_cost']:,.2f}")
        col_s3.metric("Black Swan Risk", f"{seasonal_res['black_swan_risk']:.2f}%", 
                      help="Probability of hitting the P80+ unlucky tail in ALL seasonal banners simultaneously.")
        
        st.warning(f"⚠️ **Portfolio Verdict:** A player has a **1 in {int(100/seasonal_res['black_swan_risk'])}** chance of being unlucky across all major seasonal events, potentially leading to financial collapse.")
        
        # Plot seasonal cost distribution
        fig_seasonal = px.histogram(seasonal_res['cumulative_costs'], nbins=50, 
                                   title="Seasonal Financial Load Distribution",
                                   labels={'value': 'Total Seasonal Spend ($)'})
        st.plotly_chart(fig_seasonal, use_container_width=True)

st.divider()
st.caption("Forensic Toolset v1.0.0 | Distributional Mathematics for Consumer Protection")
