from abc import ABCMeta, abstractmethod

class CallCenter():

    def __init__ (self, agents=None):
        self.agents = list()
        if agents is not None:
            self.agents += agents

    
    def _getCapacity(self, schedules: str):
        if len(self.agents) > 0:
            print('only %s agents can accept calls during %s' %(str(len(self.agents) * 80 /100), schedules))
        else:
            raise Exception('Call center has no agents')


class Chair(metaclass=ABCMeta):

    # using ABCMeta as the metaclass allows the lint to raise an error when the object is instantiated
    # instead of waiting until the abstract method is being called

    @abstractmethod # defined in the base class but does not provide any implementation
    def get_dimensions(self):
        '''the chair interface'''

class BigChair(Chair):

    def __init__ (self):
        self.height = 80    
        self.width = 80
        self.length = 80

    def get_dimensions(self):
        return {'height': self.height, 'width': self.width, 'length': self.length}

class SmallChair(Chair):

    def __init__ (self):
        self.height = 70    
        self.width = 70
        self.length = 70

    def get_dimensions(self):
        return {'height': self.height, 'width': self.width, 'length': self.length}
    
class ChairFactory:

    @staticmethod # static method belongs to a class but doesn't use the object itself
    def get_chair(chairtype):
        try:
            if chairtype == 'BigChair':
                return BigChair()
            elif chairtype == 'SmallChair':
                return SmallChair()
            raise AssertionError('Chair not found')
                
        except AssertionError as _e:
            print(_e)

bigchair = ChairFactory.get_chair('BigChair')
print(bigchair.get_dimensions())