from gail_rel_risk import calculate_relative_risk
from gail_table_4 import get_probability

def get_gail_probability(age, menarche_age, num_biopsies, first_live_birth_age, num_relatives):

    # Risk scores 
    r0 = calculate_relative_risk(age, menarche_age, num_biopsies, first_live_birth_age, num_relatives)
    r10 = calculate_relative_risk(age + 10, menarche_age, num_biopsies, first_live_birth_age, num_relatives)

    p10 = get_probability(age, r0, r10) / 100


    p1 = 1 - (1-p10)**0.1

    return p1

if __name__ == "__main__":
    risk = get_gail_probability(age=65, menarche_age=13, num_biopsies=2, first_live_birth_age=29, num_relatives=1)
    print(f"1 year risk of breast cancer is {risk*100:.2f}%")

