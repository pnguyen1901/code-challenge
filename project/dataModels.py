import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Customer:

    def __init__ (self, id, age, state, phoneNumber, numberOfKids, numberOfCars, housingStatus, householdIncome):
        self.id  = id      
        self.age = age
        self.state = state
        self.phoneNumber = phoneNumber
        self.numberOfKids = numberOfKids
        self.numberOfCars = numberOfCars
        self.housingStatus = housingStatus
        self.householdIncome = householdIncome
        self.callReceived = 0

    # special method __repr__() to display data associated with object
    def __repr__(self):
        return ('''
            id: {},
            age: {}, 
            state: {},
            phone number: {},
            number of kids: {}, 
            number of cars: {}, 
            housing status: {},
            household income: {},
            call received: {}'''
        .format(
                self.id,\
                self.age,\
                self.state,\
                self.phoneNumber,\
                self.numberOfKids,\
                self.numberOfCars,\
                self.housingStatus,\
                self.householdIncome,\
                self.callReceived
            ))

    # method to return a dictionary representation of this class
    def to_dict(self):
        return {
            'id': self.id,
            'age': self.age, 
            'state': self.state,
            'phone number': self.phoneNumber,
            'number of kids': self.numberOfKids, 
            'number of cars': self.numberOfCars, 
            'housing status': self.housingStatus,
            'household income': self.householdIncome,
            'call received': self.callReceived
        }



class Agent:

    def __init__ (self, id, age, state, housingStatus, householdIncome):
        self.id = id
        self.age = age
        self.state = state
        self.housingStatus = housingStatus
        self.householdIncome = householdIncome
        self.timeoutTimestamp = 0
        self.callReceived = 0
        self.voicemailLeft = 0

    # special method __repr__() to display data associated with object
    def __repr__(self):
        return ('''
            id: {},
            age: {}, 
            state: {},
            housing status: {},
            household income: {},
            timeout timestamp: {},
            call received: {},
            voicemails left: {}
        '''
        .format(
                self.id,\
                self.age,\
                self.state,\
                self.housingStatus,\
                self.householdIncome,\
                self.timeoutTimestamp,\
                self.callReceived,\
                self.voicemailLeft\
            ))

    # method to return a dictionary representation of this class
    def to_dict(self):
        return {
            'id': self.id,
            'age': self.age, 
            'state': self.state,
            'housing status': self.housingStatus,
            'household income': self.householdIncome,
            'call received': self.callReceived,
            'voicemail left': self.voicemailLeft,
        }
