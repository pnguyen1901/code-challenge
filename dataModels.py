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

    # method to return a dictionary representation of this class
    def to_dict(self):
        return {
            'age': self.age, 
            'state': self.state,
            'phone number': self.phoneNumber,
            'number of kids': self.numberOfKids, 
            'number of cars': self.numberOfCars, 
            'housing status': self.housingStatus,
            'household income': self.householdIncome
        }



class Agent:

    def __init__ (self, age, state, housingStatus, householdIncome):
        self.age = age
        self.state = state
        self.housingStatus = housingStatus
        self.householdIncome = householdIncome
        self.timeoutTimestamp = 0
        self.callReceived = 0
        self.voiceMailLeft = 0

    # special method __repr__() to display data associated with object
    def __repr__(self):
        return ('''
            age: {}, 
            state: {},
            housing status: {},
            household income: {},
            call received: {},
            voicemail left: {}
        '''
        .format(self.age,\
                self.state,\
                self.housingStatus,\
                self.householdIncome,\
                self.callReceived,\
                self.voiceMailLeft\
            ))

    # method to return a dictionary representation of this class
    def to_dict(self):
        return {
            'age': self.age, 
            'state': self.state,
            'housing status': self.housingStatus,
            'household income': self.householdIncome,
            'call received': self.callReceived,
            'voicemail left': self.voiceMailLeft
        }
