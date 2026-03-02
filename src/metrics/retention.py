import numpy as np

def calculate_retention_rigidity(missed_progress, daily_recoverable_progress):
    """
    Module 2: Quantify the transition from engagement to extortion using time-recovery debt.
    
    Args:
        missed_progress (float): Progress lost during absence (e.g., season points).
        daily_recoverable_progress (float): Max progress gainable per day.
        
    Returns:
        dict: OCA and Recovery Interest Rate.
    """
    oca = missed_progress / daily_recoverable_progress
    recovery_interest = (oca - 1) * 100 if oca > 1.0 else 0
    
    return {
        "oca": float(oca),
        "recovery_interest_rate": float(recovery_interest)
    }

def calculate_schedule_rigidity(login_windows, total_hours=24):
    """
    Module 2: Schedule Rigidity Index (SRI).
    Measures time-of-day constraints.
    
    Args:
        login_windows (list of tuples): List of (start_hour, end_hour) for login bonuses.
        total_hours (int): Duration of a single day (typically 24).
        
    Returns:
        float: SRI (Higher means more rigid/constrained).
    """
    constrained_hours = sum(end - start for start, end in login_windows)
    # If a player must login within narrow windows, the system is rigid.
    # SRI could be defined as 1 - (constrained_hours / total_hours)
    # Or based on the number of distinct windows (more windows = more fragmentation/pressure).
    
    sri = 1.0 - (constrained_hours / total_hours) if total_hours > 0 else 1.0
    return {
        "sri": float(sri),
        "num_windows": len(login_windows),
        "total_constrained_hours": float(constrained_hours)
    }
