from person import Person


class Simulator:

    def __init__(self):
        self.people = []

    def add_people(self, number_of_people, lower, upper):
        for i in range(number_of_people):
            self.people.append(Person.generate_person(lower, upper))

    def age_people(self, dt):
        for person in self.people:
            person.tic(dt)

    def run(self, years, dt):
        for i in range( round(years/dt) ):
            self.age_people(1)
        