from mockData import Agent, Customer
import time
import numpy as np
from faker import Faker
from functools import reduce


class CallCenter:

    def __init__ (self, noOfCustomers, noOfAgents):
        self.noOfCustomers = noOfCustomers
        self.noOfAgents = noOfAgents
        self.fake_data = Faker()
    
    @staticmethod
    def __match(customer, agents):

        return list(filter(lambda agent: agent.age[0] <= customer.age and agent.age[1] >= customer.age, agents))


    def __createCustomer(self):

        f = open('listOf50States.txt', 'r')
        # Remove all whitespace characters and split the string into a list of US states
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfCustomers):
            customer = Customer(
                    np.random.randint(18,90, size=1, dtype=int)[0],\
                    self.fake_data.random_element(elements=states),\
                    self.fake_data.phone_number(),\
                    self.fake_data.random_digit(),\
                    self.fake_data.random_digit(),\
                    self.fake_data.random_element(elements=housingStatus),\
                    np.random.randint(25000, 200000, size=1, dtype=int)[0]
                    )
            
            yield customer

    def __createAgent(self):

        f = open('listOf50States.txt', 'r')
        # Remove all whitespace characters and split the string into a list of US states
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfAgents):
            agent = Agent(
                    sorted(np.random.randint(18,90, size=2, dtype=int)),\
                    self.fake_data.random_elements(elements=states),\
                    self.fake_data.random_element(elements=housingStatus),\
                    sorted(np.random.randint(25000, 200000, size=2, dtype=int))
                    )
            
            yield agent


    def createSimulation(self):
        call_back_customers = []

        agents = list(self.__createAgent())

        for _ in range(self.noOfCustomers):
            customers = self.__createCustomer()
            current_customer = next(customers)
            matching_agents = self.__match(current_customer, agents)
            #print(matching_agents)
            
            if len(matching_agents) > 1: # if there more than 1 matching agent, randomly select one
                random_number = np.random.randint(low=0, high=len(matching_agents)-1, size=1,dtype=int)[0]
                
                random_timeout = np.random.randint(low=50, high=300, size=1, dtype=int)[0]

                selected_agent = matching_agents[random_number]
                # if the current timestamp of the agent is less than timestamp now in epoch format, the agent 
                if selected_agent.timestamp < int(round(time.time() * 1000)) and selected_agent.timestamp > 0:
                    print('agent is busy')
                    call_back_customers.append(current_customer)
                else:
                # set the timeout of this agent
                    selected_agent.timestamp = int(round(time.time() * 1000)) + random_timeout

        print(call_back_customers)
        # calculate agent utilization
        agentUtilized = len(list(filter(lambda agent: agent.timestamp != 0, agents)))
        agentUtilization = agentUtilized/len(agents) * 100
        print('Agent Utilization: %s %%' %agentUtilization)


noOfCustomers = 1000
noOfAgents = 20

newSimulation = CallCenter(noOfCustomers, noOfAgents)
newSimulation.createSimulation()


'''
    filter based on two criteria
    1. attribute matches
    2. current timestamp > timeout attribute

    list of available based on attributes
    length of list
    use Random module to generate a random number
    pick that agent
    reset the timeout based on 50 and 300 miliseconds 
'''