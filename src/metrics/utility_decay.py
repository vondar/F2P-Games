def calculate_utility_decay(acquisition_cost, expected_meta_lifespan_days):
    """
    Calculates the 'Utility Shelf-Life' metric.
    Translates a one-time purchase into a daily 'Meta-Relevance' subscription cost.
    
    Args:
        acquisition_cost (float): Total cost to acquire the item ($).
        expected_meta_lifespan_days (int): Days until item is expected to be power-crept.
        
    Returns:
        dict: {
            "daily_relevance_cost": float,
            "monthly_relevance_cost": float,
            "shelf_life_days": int
        }
    """
    if expected_meta_lifespan_days <= 0:
        return {
            "daily_relevance_cost": float('inf'),
            "monthly_relevance_cost": float('inf'),
            "shelf_life_days": 0
        }
        
    daily_cost = acquisition_cost / expected_meta_lifespan_days
    
    return {
        "daily_relevance_cost": float(daily_cost),
        "monthly_relevance_cost": float(daily_cost * 30.44), # Average month
        "shelf_life_days": expected_meta_lifespan_days
    }
