import pytest
import numpy as np
from src.metrics.risk_metrics import calculate_risk_metrics
from src.metrics.retention import calculate_retention_rigidity, calculate_schedule_rigidity
from src.metrics.friction import calculate_incentive_gap, calculate_conversion_loss_factor

def test_risk_metrics():
    # Simple data: 100 trials, median is 50.
    sim_data = np.arange(1, 101) # 1 to 100
    metrics = calculate_risk_metrics(sim_data)
    
    # p95 threshold is 95.05. Tail values are 96, 97, 98, 99, 100
    # CTE95 = (96+97+98+99+100)/5 = 98.0
    assert metrics['median'] == 50.5
    assert metrics['p95'] == pytest.approx(95.05)
    assert metrics['cte95'] == pytest.approx(98.0)
    assert metrics['wrr'] == pytest.approx(98.0 / 50.5)

def test_retention_rigidity():
    # OCA = Missed / Daily Recoverable
    # Missed 100 points, can recover 50 per day. OCA = 2.0. Interest = 100%
    metrics = calculate_retention_rigidity(100, 50)
    assert metrics['oca'] == 2.0
    assert metrics['recovery_interest_rate'] == 100.0
    
    # Missed 50 points, can recover 50 per day. OCA = 1.0. Interest = 0%
    metrics = calculate_retention_rigidity(50, 50)
    assert metrics['oca'] == 1.0
    assert metrics['recovery_interest_rate'] == 0.0

def test_schedule_rigidity():
    # 2 windows of 1 hour each. Total constrained = 2. Total = 24. SRI = 1 - 2/24 = 0.9166
    login_windows = [(10, 11), (18, 19)]
    metrics = calculate_schedule_rigidity(login_windows)
    assert metrics['sri'] == pytest.approx(1 - 2/24)
    assert metrics['num_windows'] == 2

def test_incentive_gap():
    # Required cost 2500, packs are [500, 1000, 2000, 5000]
    # Closest lower pack is 2000. Gap = 2500 - 2000 = 500
    available_packs = [500, 1000, 2000, 5000]
    metrics = calculate_incentive_gap(2500, available_packs)
    assert metrics['ig'] == 500.0
    assert metrics['closest_lower_pack'] == 2000.0
    
    # Required cost 5000, exact match with pack size (though the metric looks for strictly lower)
    # Closest lower pack is 2000. Gap = 5000 - 2000 = 3000
    metrics = calculate_incentive_gap(5000, available_packs)
    assert metrics['ig'] == 3000.0

def test_conversion_loss():
    # 1 USD : 1.64 Gems (2 decimals), 1 Gem : 2.5 Tokens (1 decimal)
    # Complexity = 2 + 1 = 3
    exchange_rates = {"USD_TO_GEM": 1.64, "GEM_TO_TOKEN": 2.5}
    metrics = calculate_conversion_loss_factor(exchange_rates)
    assert metrics['conversion_complexity_score'] == 3.0
    assert metrics['num_exchange_steps'] == 2
