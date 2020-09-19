from faker import Faker

fake_data = Faker()


class Customer:

    def __init__ (self, age, state, numberOfKids, numberOfCars, householdIncome):
        self.age = age
        self.state = state
        self.numberOfKids = numberOfKids
        self.numberOfCars = numberOfCars
        self.householdIncome = householdIncome



for _ in range(0,20):
    profile = fake_data.simple_profile()
    for k, v in profile.items():
        print('{}: {}'.format(k, v))