import numpy as np
from states import state
from life_table_data import death_p
from dtree import classifier
from BCSC_encoder import encode_inputs

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

    # https://www.gov.uk/government/news/hundreds-of-thousands-of-women-experiencing-menopause-symptoms-to-get-cheaper-hormone-replacement-therapy
    # https://www.nhs.uk/medicines/hormone-replacement-therapy-hrt/when-to-take-hormone-replacement-therapy-hrt/
    CHANCE = 14.6 # 15% * 98%

    # if women menopuase prematurely they should be on HRT until 51 by NICE guidelines
    if menopause <= 45:
        return 51 - menopause
    
    if np.random.uniform(low=0, high=100) > CHANCE:
        return 0
    return np.random.uniform(low=2, high=5) # most women in this range so pick at random

def generate_surmeno():
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC9433845/
    CHANCE = 9.8
    if np.random.uniform(low=0, high=100) < CHANCE:
        return True
    return False


class Person:

    def __init__(
            self, age, menopause, menarche,
            ethn, chld_b, hrt, relatives, bmi20, bmi50, bmi80, scheme
        ):
        self.age = age # done
        self.menopause = menopause # done
        self.menarche = menarche # done
        self.ethn = ethn # done
        self.chld_b = chld_b # done
        self.hrt = hrt # done
        self.relatives = relatives #done
        self.biopsies = 0
        self.procedures = 0
        self.density = 1 # do
        self.surmeno = generate_surmeno()
        self.bmi20 = bmi20
        self.bmi50 = bmi50
        self.bmi80 = bmi80
        self.screen_cost = 0
        self.risk_level = 1
        self.risks = scheme
        self.state = state(self.age, death_p())
        self.classifier = classifier()
    
    @classmethod
    def generate_person(cls, age, scheme):
        menopause = generate_menopause()
        menarche = generate_menarche()
        ethnicity = generate_ethnicity()
        relatives = generate_relatives()
        chld_b = generate_childbirth()
        hrt = generate_HRT(menopause)
        # avg from https://digital.nhs.uk/data-and-information/publications/statistical/health-survey-for-england/2022-part-2
        #std from https://www.researchgate.net/publication/306049161_Eating_patterns_and_prevalence_of_obesity_Lessons_learned_from_the_Malaysian_Food_Barometer
        bmi50 = np.random.normal(28.4, 4.572)
        bmi20 = np.random.normal(24.9, 4.572)
        bmi80 = np.random.normal(27.5, 4.572)
        return cls(age, menopause, menarche, ethnicity, chld_b, hrt, relatives, bmi20, bmi50, bmi80, scheme)

    def get_state(self):
        return self.state.state

    def is_menopausal(self):
        return self.age >= self.menopause
    
    def on_hrt(self):
        return self.age >= self.menopause and self.age <= self.menopause + self.hrt
    
    def get_bmi(self):
        if self.age <= 20:
            return self.bmi20
        elif self.age >= 80:
            return self.bmi80
        elif self.age <= 50:
            return self.bmi20 + (self.bmi50 - self.bmi20) * ((self.age - 20) / (50 - 20))
        else:
            return self.bmi50 + (self.bmi80 - self.bmi50) * ((self.age - 50) / (80 - 50))
    
    def tic(self, dt=1):
        self.age += dt
        risks = {"age": self.age, 
                 "age_at_menarche": self.menarche, 
                 "num_biopsies": self.biopsies, 
                 "age_at_first_birth": self.chld_b, 
                 "num_first_degree_relatives": self.relatives
                 }
        
        due_screen = self.check_screen()
        if due_screen and np.random.uniform(0, 100) < 70:
            self.screen_cost += 57.69
        else:
            dur_screen = False

        self.state.check_transistion(risks, self.age, due_screen, dt)

    def check_screen(self):


        risk_data = encode_inputs(
            self.is_menopausal(),
            self.age,
            self.density,
            self.ethn,
            self.get_bmi(),
            self.chld_b,
            self.relatives,
            self.procedures,
            False,
            self.surmeno,
            self.on_hrt()
        )

        catagory = self.classifier.risk_prediction(risk_data)
        self.risk_level = catagory

        return (self.age - self.risks[catagory][0]) % self.risks[catagory][1] == 0 and self.age >= self.risks[catagory][0]

    

if __name__ == "__main__":
    e = Person.generate_person(30, 30.1)
    print(f"Age: {e.age}")
    print(f"ethnicity: {e.ethn}")
    print(f"first child birth: {e.chld_b}")
    print(f"menarche: {e.menarche}")


    
