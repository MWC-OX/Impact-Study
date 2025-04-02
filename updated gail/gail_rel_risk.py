def categorize_menarche_age(age):
    """Categorizes menarche age into Gail Model categories."""
    if age >= 14:
        return 14  # Coded as (0)
    elif 12 <= age <= 13:
        return 12  # Coded as (1)
    else:
        return 11  # Coded as (2)

def categorize_first_live_birth_age(age):
    """Categorizes first live birth age into Gail Model categories."""
    if age < 20:
        return 0  # <20 (0)
    elif 20 <= age <= 24:
        return 1  # 20-24 (1)
    elif 25 <= age <= 29 or age == -1:  # Nulliparous (no birth) is grouped here
        return 2  # 25-29 or nulliparous (2)
    else:
        return 3  # ≥30 (3)

def categorize_num_relatives(count):
    """Ensures number of first-degree relatives falls into 0, 1, or 2+ categories."""
    return min(count, 2)  # 2+ relatives are grouped together

def calculate_relative_risk(age, menarche_age, num_biopsies, first_live_birth_age, num_relatives):
    """
    Calculates the relative risk using the Gail Model risk factors.

    Parameters:
    age (int): Current age of the woman.
    menarche_age (int): Age at menarche (first menstrual period).
    num_biopsies (int): Number of breast biopsies.
    first_live_birth_age (int): Age at first live birth (-1 for nulliparous).
    num_relatives (int): Number of first-degree relatives with breast cancer.

    Returns:
    float: Calculated relative risk.
    """

    # Convert actual ages into categories
    menarche_cat = categorize_menarche_age(menarche_age)
    birth_cat = categorize_first_live_birth_age(first_live_birth_age)
    relatives_cat = categorize_num_relatives(num_relatives)

    # Coefficients extracted from the table
    coef_menarche = {14: 1.000, 12: 1.099, 11: 1.207}  # 14+ (0), 12-13 (1), <12 (2)
    coef_biopsies_under_50 = {0: 1.000, 1: 1.698, 2: 2.882}  # Age < 50 years
    coef_biopsies_over_50 = {0: 1.000, 1: 1.273, 2: 1.620}  # Age ≥ 50 years
    
    # Combined coefficient for age at first live birth & number of relatives
    coef_birth_relatives = {
        (0, 0): 1.000, (0, 1): 2.607, (0, 2): 6.798,  # <20
        (1, 0): 1.244, (1, 1): 2.681, (1, 2): 5.775,  # 20-24
        (2, 0): 1.548, (2, 1): 2.756, (2, 2): 4.907,  # 25-29 or nulliparous
        (3, 0): 1.927, (3, 1): 2.834, (3, 2): 4.169,  # ≥30
    }

    # Get the correct coefficient values
    menarche_risk = coef_menarche[menarche_cat]
    biopsy_risk = coef_biopsies_under_50.get(num_biopsies, 2.882) if age < 50 else coef_biopsies_over_50.get(num_biopsies, 1.620)
    birth_relatives_risk = coef_birth_relatives.get((birth_cat, relatives_cat), 4.169)

    # Calculate the final relative risk
    relative_risk = menarche_risk * biopsy_risk * birth_relatives_risk

    return relative_risk

# Example usage:
if __name__ == "__main__":
    risk = calculate_relative_risk(age=45, menarche_age=13, num_biopsies=1, first_live_birth_age=26, num_relatives=0)
    print(f"Calculated Relative Risk: {risk:.3f}")
