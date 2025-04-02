import numpy as np

def get_probability(initial_age, initial_risk, final_risk):
    """
    Returns the 10-year probability of developing breast cancer given the initial age,
    initial risk factor, and final risk factor (10 years later).
    If the exact age or risk factor is not in the table, it will interpolate between values.
    """
    # Table data extracted from the image (subset for demonstration, add full data as needed)
    table = {
        20: {1.0: 0.0, 2.0: 0.1, 5.0: 0.2, 10.0: 0.5, 20.0: 1.0, 30.0: 1.4},
        30: {1.0: 0.5, 2.0: 0.9, 5.0: 2.3, 10.0: 4.4, 20.0: 8.7, 30.0: 12.8},
        40: {1.0: 1.2, 2.0: 2.5, 5.0: 6.1, 10.0: 11.8, 20.0: 22.2, 30.0: 31.3},
        50: {1.0: 1.6, 2.0: 3.1, 5.0: 7.6, 10.0: 14.6, 20.0: 27.1, 30.0: 37.7},
        60: {1.0: 1.8, 2.0: 3.6, 5.0: 8.6, 10.0: 16.5, 20.0: 30.1, 30.0: 41.5},
        70: {1.0: 1.4, 2.0: 2.7, 5.0: 6.7, 10.0: 12.9, 20.0: 24.1, 30.0: 33.7},
    }

    if initial_age > 70:
        initial_age = 70
    
    # Get the closest ages available
    available_ages = sorted(table.keys())
    if initial_age in table:
        age_data = table[initial_age]
    else:
        lower_age = max(a for a in available_ages if a < initial_age)
        upper_age = min(a for a in available_ages if a > initial_age)
        lower_data = table[lower_age]
        upper_data = table[upper_age]
        
        # Interpolate between the two ages for each risk factor
        age_data = {
            risk: np.interp(initial_age, [lower_age, upper_age], [lower_data[risk], upper_data[risk]])
            for risk in set(lower_data.keys()).intersection(set(upper_data.keys()))
        }
    
    # Get the closest risk factors available
    available_risks = sorted(age_data.keys())
    if initial_risk in age_data:
        probability = age_data[initial_risk]
    else:
        lower_risk = max(r for r in available_risks if r < initial_risk)
        upper_risk = min(r for r in available_risks if r > initial_risk)
        probability = np.interp(initial_risk, [lower_risk, upper_risk], [age_data[lower_risk], age_data[upper_risk]])
    
    return probability


if __name__ == "__main__":
    # Example usage
    initial_age = 55
    initial_risk = 2.165
    final_risk = 2.5  # Not directly used in the lookup, but could be extended
    p10 = get_probability(initial_age, initial_risk, final_risk)
    print(f"The 10-year probability is {p10:.2f}%")

