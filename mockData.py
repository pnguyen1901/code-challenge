from faker import Faker
import json
import numpy as np

fake_data = Faker()


class Customer:

    def __init__ (self, age, state, numberOfKids, numberOfCars, householdIncome):
        self.age = age
        self.state = state
        self.numberOfKids = numberOfKids
        self.numberOfCars = numberOfCars
        self.householdIncome = householdIncome

    # special method __repr__() to display data associated with object
    def __repr__(self):
        return ('''
            age: {}, 
            state: {}, 
            number of kids: {}, 
            number of cars: {}, 
            household income: {}'''
        .format(self.age, self.state, self.numberOfKids, self.numberOfCars, self.householdIncome))



f = open('listOf50States.txt', 'r')
# Remove all whitespace characters and split the string into a list of US states
states = f.read().replace(' ', '').split(',')


for _ in range(0,20):
    customer = Customer(
            np.random.randint(18,90, size=1, dtype=int)[0],\
            fake_data.random_element(elements=states),\
            fake_data.random_digit(),\
            fake_data.random_digit(),\
            np.random.randint(25000, 200000, size=1, dtype=int)[0]
            )
    print(customer)