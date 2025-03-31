import numpy as np

def gail_model_risk(age, age_at_menarche, age_at_first_birth, num_first_degree_relatives, num_biopsies, atypical_hyperplasia, race):
    """
    Estimate the risk of developing breast cancer using the Gail Model.
    
    Parameters:
    - age: Current age of the woman.
    - age_at_menarche: Age at first menstrual period.
    - age_at_first_birth: Age at first live birth.
    - num_first_degree_relatives: Number of first-degree relatives with breast cancer.
    - num_biopsies: Number of breast biopsies.
    - atypical_hyperplasia: Presence of atypical hyperplasia (True/False).
    - race: Race/ethnicity of the woman.
    
    Returns:
    - Estimated risk percentage of developing breast cancer.
    """
    # https://academic.oup.com/jnci/article-abstract/81/24/1879/1019887?redirectedFrom=fulltext
    intercept = -7.63
    coef_age = 0.094
    coef_age_at_menarche = 0.529
    coef_age_at_first_birth = 0.473
    coef_num_first_degree_relatives = 0.693
    coef_num_biopsies = 0.389
    coef_atypical_hyperplasia = 0.875
    coef_race = {
        "Caucasian": 0,
        "African American": 0.126,
        "Asian": -0.288,
        "Hispanic": -0.288,
        "Other": 0
    }
    
    # Calculate the log-odds of developing breast cancer
    log_odds = (intercept +
                coef_age * age +
                coef_age_at_menarche * (age_at_menarche < 12) +
                coef_age_at_first_birth * (age_at_first_birth > 30) +
                coef_num_first_degree_relatives * num_first_degree_relatives +
                coef_num_biopsies * num_biopsies +
                coef_atypical_hyperplasia * atypical_hyperplasia +
                coef_race.get(race, 0))
    
    # Convert log-odds to probability
    risk = 1 / (1 + np.exp(-log_odds))
    
    return risk

# Example usage
risk = gail_model_risk(age=40, age_at_menarche=13, age_at_first_birth=28, num_first_degree_relatives=1, num_biopsies=2, atypical_hyperplasia=True, race="Caucasian")
print(f"Estimated risk of developing breast cancer: {risk:.2%}")