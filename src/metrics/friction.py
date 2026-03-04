import numpy as np

def calculate_incentive_gap(required_cost, available_packs):
    """
    Module 3: Incentive Gap (IG).
    Measures forced surplus spending by comparing required cost with available pack sizes.
    
    Args:
        required_cost (float): Total cost for a target acquisition.
        available_packs (list of float): Sorted list of available currency pack amounts.
        
    Returns:
        dict: Incentive Gap (Required - Closest Lower Pack).
    """
    if not available_packs:
        return {"ig": 0.0}
    
    # Find the largest pack smaller than the required cost
    lower_packs = [p for p in available_packs if p < required_cost]
    
    if not lower_packs:
        # If no packs are smaller than required, the gap is zero or based on the smallest pack.
        return {"ig": 0.0, "closest_lower_pack": 0.0}
    
    closest_lower_pack = max(lower_packs)
    ig = required_cost - closest_lower_pack
    
    return {
        "ig": float(ig),
        "closest_lower_pack": float(closest_lower_pack),
        "required_cost": float(required_cost)
    }

def calculate_loss_aversion_index(current_shards, total_shards_required, cost_per_pull):
    """
    Calculates the 'Loss Aversion Index' (LAI).
    Quantifies the psychological sunk cost of partial progress.
    """
    if total_shards_required <= 0:
        return {"lai": 0.0, "perceived_value_multiplier": 1.0}
        
    completion_ratio = current_shards / total_shards_required
    
    # Mathematical value of the next pull is 1/total_shards of the item.
    # Psychological value increases non-linearly as completion_ratio approaches 1.0.
    # LAI = (1 / (1 - completion_ratio)) if completion_ratio < 1 else inf
    
    if completion_ratio >= 1.0:
        perceived_multiplier = float('inf')
    else:
        # Heuristic: Perceived value multiplier grows as completion nears.
        # At 8/10 (80%), the next shard feels 5x more valuable than the first.
        perceived_multiplier = 1.0 / (1.0 - completion_ratio)
        
    return {
        "completion_ratio": float(completion_ratio),
        "perceived_value_multiplier": float(perceived_multiplier),
        "lai_score": float(perceived_multiplier * completion_ratio), # Weighted by progress
        "abandonment_penalty_usd": float(completion_ratio * total_shards_required * cost_per_pull)
    }

def calculate_top_up_pressure(current_balance, available_packs, minimum_item_cost):
    """
    Calculates the 'Top-Up Pressure Index'.
    The minimum additional spend required to bring a currency balance to zero
    given that the cheapest next item costs more than the leftover balance.
    """
    if current_balance >= minimum_item_cost:
        return {
            "top_up_required": 0.0,
            "pressure_index": 0.0,
            "residual_utility": float(current_balance)
        }
    
    needed = minimum_item_cost - current_balance
    
    # Find the cheapest pack that covers the 'needed' amount
    valid_packs = [p for p in available_packs if p >= needed]
    if not valid_packs:
        cheapest_pack = min(available_packs) # Forced to buy multiple or larger
    else:
        cheapest_pack = min(valid_packs)
        
    return {
        "top_up_required": float(cheapest_pack),
        "pressure_index": float(cheapest_pack / minimum_item_cost if minimum_item_cost > 0 else 0),
        "residual_utility": float(current_balance)
    }

def calculate_social_proof_hallucination(ritual_count, delay_per_ritual_sec=5.0):
    """
    Module 3: Social Proof Hallucination Index.
    Quantifies the psychological friction of 'rituals' (e.g., tapping skins, 
    not skipping animations) that create a false sense of control.
    
    Args:
        ritual_count (int): Number of ritual actions performed.
        delay_per_ritual_sec (float): Estimated time delay per action.
        
    Returns:
        dict: Hallucination metrics.
    """
    total_delay = ritual_count * delay_per_ritual_sec
    # The 'Hallucination' is that these rituals affect the PRNG.
    # We quantify this as 'Wasted Cognitive Time' per session.
    
    return {
        "ritual_count": int(ritual_count),
        "total_delay_sec": float(total_delay),
        "cognitive_friction_index": float(ritual_count * 0.15), # Heuristic: 15% increase in perceived engagement per ritual
        "verdict": "RITUAL NOISE DETECTED: IRRELEVANT TO PRNG"
    }

def get_grocery_equivalent(cost_usd, region_data):
    """
    Translates USD cost into visceral 'Grocery' and 'Rent' equivalents
    for a given region.
    """
    median_daily = region_data.get("median_daily_income_usd", 1.0)
    big_mac = region_data.get("big_mac_price_usd", 5.0)
    
    # Heuristics for visceral comparison
    # 1 week of groceries approx 1.5 days of median income (conservative)
    weekly_groceries_usd = median_daily * 1.5
    # Monthly rent approx 10 days of median income
    monthly_rent_usd = median_daily * 10.0
    
    weeks_groceries = cost_usd / weekly_groceries_usd if weekly_groceries_usd > 0 else 0
    months_rent = cost_usd / monthly_rent_usd if monthly_rent_usd > 0 else 0
    big_macs = cost_usd / big_mac if big_mac > 0 else 0
    
    return {
        "weeks_groceries": float(weeks_groceries),
        "months_rent": float(months_rent),
        "big_macs": int(big_macs)
    }

def calculate_conversion_loss_factor(exchange_rates):
        if isinstance(rate_data, dict):
            rate = rate_data.get("base", 1.0)
            bonus = rate_data.get("bonus", 0.0)
            # Bonus currency adds "phantom value" that makes mental math harder
            if bonus > 0:
                total_bonus_obfuscation += 1.5 # Heuristic penalty for bonus complexity
        else:
            rate = rate_data
            
        # Heuristic: fractional part complexity
        str_rate = str(rate)
        if '.' in str_rate:
            decimal_places = len(str_rate.split('.')[1])
            complexity += decimal_places
            
    return {
        "conversion_complexity_score": float(complexity),
        "bonus_obfuscation_penalty": float(total_bonus_obfuscation),
        "total_friction_score": float(complexity + total_bonus_obfuscation),
        "num_exchange_steps": len(exchange_rates)
    }
