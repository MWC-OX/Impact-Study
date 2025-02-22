from person import Person


class Simulator:

    def __init__(self):
        self.data = []
        

    def simulate_person(self, upper=80, lower=20, dt=1):

        subject = Person.generate_person(upper, lower)
        result = {}

        result["race"] = subject.get_race()

        while subject.get_state() != "DEAD":

            result["age"].append(subject.get_age())
            result["state"].append(subject.get_state())
            result["risk score"].append(subject.get_risk_score())
            result["bmi"].append(subject.get_bmi())

            subject.tic(dt)
        
        result["costs"] = subject.b_cancer_costs

        self.data.append(result)


    def simulate_population(self, n=1000, upper=80, lower=20, dt=1):

        self.clear_data()

        for _ in range(n):
            self.simulate_person(upper, lower, dt)

        return self.data
    
    def clear_data(self):
        self.data = []

    

