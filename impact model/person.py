import numpy as np

def generate_age(lower, upper):
    return round(np.random.uniform(low=lower, high=upper))

def generate_menopause():
    # https://pubmed.ncbi.nlm.nih.gov/29460096/
    MEAN = 51.4
    STD = 3.3

    UPPER = 60
    LOWER = 40

    menopause = np.random.normal(MEAN, STD)

    if menopause > UPPER:
        return UPPER
    if menopause < LOWER:
        return LOWER
    return menopause

def generate_menarche():
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC2994234/
    MEAN = 12.7
    STD = 1.5

    UPPER = 20
    LOWER = 7

    menarche = np.random.normal(MEAN, STD)

    if menarche > UPPER:
        return UPPER
    if menarche < LOWER:
        return LOWER
    return menarche

def generate_ethnicity():
    # https://www.ethnicity-facts-figures.service.gov.uk/uk-population-by-ethnicity/national-and-regional-populations/population-of-england-and-wales/latest/#by-ethnicity-19-groups
    ethnicities = {
        "WHITE": 81.7,
        "ASIAN": 9.3,
        "BLACK": 4,
        "OTHER/MIXED": 2.1 + 2.9
    }

    ethnicity_list = list(ethnicities.keys())
    weight_list = list(ethnicities.values())

    total_weight = sum(weight_list)
    normalized_weights = [weight / total_weight for weight in weight_list]


    return np.random.choice(ethnicity_list, p=normalized_weights)

def generate_childbirth():
    # using 2017
    # https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/bulletins/birthcharacteristicsinenglandandwales/2021
    # https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/adhocs/009572standarddeviationofthemeanageofmotherat1st2nd3rd4thand5thbirth1969to2017englandandwales
    # https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/conceptionandfertilityrates/bulletins/childbearingforwomenbornindifferentyearsenglandandwales/2021and2022
    CHANCE = 84 # 84% of women have children
    STD = 5.91
    MEAN = 30.5
    UPPER = 47
    LOWER = 16

    if np.random.uniform(low=0, high=100) > CHANCE:
        return -1
    
    age = np.random.normal(MEAN, STD)

    if age > UPPER:
        return UPPER
    if age < LOWER:
        return LOWER
    return age
    
def generate_bcra(type, eth):

    # https://pmc.ncbi.nlm.nih.gov/articles/PMC2771545/
    if type == 1:
        RISK = {
            "WHITE": 6.9, # using "western europen, closest representation to uk white population"
            "ASIAN": 6.3,
            "BLACK": 10.2, # used african 
            "OTHER/MIXED": (9.6 + 6.1 + 7.4)/3 # avaraged unaccounted for population
        }
    
    if type == 2:
        RISK = {
        "WHITE": 5.2,
        "ASIAN": 6.3,
        "BLACK": 5.7,
        "OTHER/MIXED": (3.3 + 5.9 + 5.4)/3
        }

    if np.random.uniform(low=0, high=100) < RISK[eth]:
        return True
    return False

def generate_relatives():
    # derived from dataset, appeared to be independant of any other factors, should T test
    NUM = [0, 1, 2]
    CHANCE = [0.8466, 0.1457, 0.0077]

    return np.random.choice(NUM, p=CHANCE)

def generate_HRT(menopause):

    # https://pmc.ncbi.nlm.nih.gov/articles/PMC5198659/
    # https://www.gov.uk/government/news/hundreds-of-thousands-of-women-experiencing-menopause-symptoms-to-get-cheaper-hormone-replacement-therapy
    CHANCE = 15 # 15%

    # if women menopuase prematurely they should be on HRT until 51 by NICE guidelines
    if menopause < 51:
        return 51 - menopause
    
    if np.random.uniform(low=0, high=100) > CHANCE:
        return 0
    return np.random.uniform(low=2, high=6) # most women in this range so pick at random


class Person:

    def __init__(
            self, age, menopause, menarche, b_density,
            ethn, chld_b, hrt, bmi, bcra1, bcra2, relatives
        ):
        self.age = age # done
        self.menopause = menopause # done
        self.menarche = menarche # done
        self.b_density = b_density
        self.ethn = ethn # done
        self.chld_b = chld_b # done
        self.hrt = hrt # done
        self.bmi = bmi 
        self.bcra1 = bcra1 # done
        self.bcra2 = bcra2 # done
        self.relatives = relatives #done
        self.b_cancer_costs = 0
    
    @classmethod
    def generate_person(cls, lower, upper):
        age = generate_age(lower, upper)
        menopause = generate_menopause()
        menarche = generate_menarche()
        ethnicity = generate_ethnicity()
        brca1 = generate_bcra(1, ethnicity)
        brca2 = generate_bcra(2, ethnicity)
        relatives = generate_relatives()

    def get_state(self):
        raise NotImplementedError

    

    def is_menopausal(self):
        return self.age > self.menopause
    
