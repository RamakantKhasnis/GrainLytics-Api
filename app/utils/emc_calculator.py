import math

# Modified Chung-Pfost Equation Constants for specific grains
# E, F, C are specific thermal and moisture constants.
# These values are standard approximations used in agricultural storage science.
GRAIN_CONSTANTS = {
    "wheat": {"E": 33.1, "F": 5.8, "C": 30.2},
    "corn":  {"E": 33.6, "F": 5.2, "C": 30.2},
    "rice":  {"E": 32.5, "F": 4.6, "C": 28.5},
    "barley": {"E": 32.9, "F": 5.4, "C": 30.0},
    "soybeans": {"E": 31.0, "F": 6.1, "C": 31.5}
}

def calculate_emc(grain_type: str, temperature_c: float, humidity_percent: float) -> float:
    """
    Calculates the Equilibrium Moisture Content (EMC) using the Modified Chung-Pfost Equation.
    Returns the EMC percentage. If calculation fails due to extreme values, returns a fallback 0.0.
    """
    grain = grain_type.lower()
    
    # If the grain isn't in our database, fallback to wheat as a general baseline
    if grain not in GRAIN_CONSTANTS:
        grain = "wheat"
        
    constants = GRAIN_CONSTANTS[grain]
    E = constants["E"]
    F = constants["F"]
    C = constants["C"]
    
    # Humidity must be a decimal between 0 and 1
    # We clamp it slightly below 1 to avoid math.log(1) which is 0 and could cause Log Domain Errors.
    rh = max(0.01, min(0.99, humidity_percent / 100.0))
    
    try:
        # Step 1: inner = -(T + C) * ln(RH)
        # Because RH is between 0 and 1, ln(RH) is negative. The negative sign makes it positive.
        inner = -(temperature_c + C) * math.log(rh)
        
        # Step 2: EMC = E - F * ln(inner)
        if inner <= 0:
            return 0.0 # Extreme impossible weather scenario
            
        emc_value = E - F * math.log(inner)
        
        # Ensure we return a logical moisture percentage (e.g. 5% to 30%)
        return round(max(0.0, min(100.0, emc_value)), 2)
        
    except Exception as e:
        print(f"EMC Calculation Error: {e}")
        return 0.0

def assess_storage_risk(emc_value: float, grain_type: str) -> str:
    """
    A basic risk analyzer comparing calculated EMC against safe storage thresholds.
    """
    grain = grain_type.lower()
    
    # Safe EMC thresholds vary, but generally staying below 13-14% is safe.
    safe_thresholds = {
        "wheat": 14.0,
        "corn": 15.0,
        "rice": 14.0,
        "barley": 13.0,
        "soybeans": 13.0
    }
    
    threshold = safe_thresholds.get(grain, 14.0)
    
    if emc_value > threshold + 3.0:
        return "CRITICAL RISK: Severe moisture accumulation. Fungal growth imminent."
    elif emc_value > threshold:
        return f"WARNING: Moisture content ({emc_value}%) is exceeding secure biological threshold ({threshold}%)."
    else:
        return f"SAFE: Grain moisture ({emc_value}%) is holding below the danger threshold."
