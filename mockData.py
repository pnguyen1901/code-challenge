from faker import Faker
import json
import numpy as np
import time
from utils import runInBackground

fake_data = Faker()


class Customer:

    def __init__ (self, age, state, phoneNumber, numberOfKids, numberOfCars, housingStatus, householdIncome):
        self.age = age
        self.state = state
        self.phoneNumber = phoneNumber
        self.numberOfKids = numberOfKids
        self.numberOfCars = numberOfCars
        self.housingStatus = housingStatus
        self.householdIncome = householdIncome

    # special method __repr__() to display data associated with object
    def __repr__(self):
        return ('''
            age: {}, 
            state: {},
            phone number: {},
            number of kids: {}, 
            number of cars: {}, 
            housing status: {},
            household income: {}'''
        .format(self.age,\
                self.state,\
                self.phoneNumber,\
                self.numberOfKids,\
                self.numberOfCars,\
                self.housingStatus,\
                self.householdIncome\
            ))



class Agent:

    def __init__ (self, age, state, housingStatus, householdIncome):
        self.age = age
        self.state = state
        self.housingStatus = housingStatus
        self.householdIncome = householdIncome
        self.timestamp = 0
