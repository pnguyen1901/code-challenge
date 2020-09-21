from dataModels import Agent, Customer
import time
import numpy as np
from faker import Faker
from functools import reduce
import pandas as pd


class CallCenter:

    def __init__ (self, noOfCustomers, noOfAgents):
        self.noOfCustomers = noOfCustomers
        self.noOfAgents = noOfAgents
        self.fake_data = Faker()
    

    @staticmethod
    def __match(customer, agents):

        return list(filter(lambda agent: agent.age[0] <= customer.age and agent.age[1] >= customer.age, agents))


    @staticmethod
    def __returnCustomerVoicemail(customer):
        customerAvailable = False

        while customerAvailable == False:
            customer.callReceived += 1
            customerAvailable = np.random.choice([True, False], size=1, p=[0.2, 0.8])[0]

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


    def __outputResults(self, customers, agents):
        
        customersDf = pd.DataFrame.from_records([customer.to_dict() for customer in customers])
        agentsDf = pd.DataFrame.from_records([agent.to_dict() for agent in agents])

        # Create a Pandas Excel writer using Xlsxwriter as the engine.
        writer = pd.ExcelWriter('output_results.xlsx', engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        customersDf.to_excel(writer, sheet_name='Customers', index=True)
        agentsDf.to_excel(writer, sheet_name='Agents', index=True)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
    

    def createSimulation(self):

        agents = list(self.__createAgent())
        customers = list(self.__createCustomer())

        for customer in customers:
            
            matching_agents = self.__match(customer, agents)
            
            if len(matching_agents) > 1: # if there more than 1 matching agent, randomly select one
                random_number = np.random.randint(low=0, high=len(matching_agents)-1, size=1,dtype=int)[0]
                
                random_timeout = np.random.randint(low=50, high=300, size=1, dtype=int)[0]

                selected_agent = matching_agents[random_number]

                # Increment number of calls this agent receives by 1.
                selected_agent.callReceived += 1
                
                # if the current timestamp of the agent is less than timestamp now in epoch format
                # the agent is busy, voicemail will be left.
                if selected_agent.timeoutTimestamp < int(round(time.time() * 1000)) and selected_agent.timeoutTimestamp > 0:
                    print('agent is busy')
                    selected_agent.voiceMailLeft += 1
                    self.__returnCustomerVoicemail(customer)
                    #call_back_customers.append(customer)
                else:
                # set the timeout of this agent
                    selected_agent.timeoutTimestamp = int(round(time.time() * 1000)) + random_timeout
                    
            # randomly sleep under 30 miliseconds between each calls.
            sleepTime = np.random.randint(low=0, high=30, size=1, dtype=int)[0]
            time.sleep(sleepTime/1000)

        # calculate agent utilization
        agentUtilized = list(filter(lambda agent: agent.timeoutTimestamp != 0, agents))
        agentUtilization = len(agentUtilized)/len(agents) * 100
        print('Agent Utilization: %s %%' %agentUtilization)

        # Output the results into an Excel file
        self.__outputResults(customers, agents)


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