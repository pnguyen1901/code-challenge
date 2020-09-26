from .dataModels import Agent, Customer
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
        self.statesFilePath = 'assets/listOf50States.txt'

    @staticmethod
    def match(customer, agents):

        return list(filter(lambda agent: agent.age[0] <= customer.age and agent.age[1] >= customer.age, agents))


    # def __returnCustomerVoicemail(self, agents):

    #     for agent in agents:
    #         agent.timeoutTimestamp = int(round(time.time() * 1000)) + 50
    #         customerAvailable = np.random.choice([True, False], size=1, p=[0.2, 0.8])[0]
    #         customer = list(filter(lambda customer: customer.id == agent.voiceMails[0]['customerId'], self.customers))[0]
    #         customer.callReceived += 1
    #         if customerAvailable:
    #             agent.voiceMails.pop(0)

        #customerAvailable = False

        # while customerAvailable == False:
        #     customer.callReceived += 1
        #     customerAvailable = np.random.choice([True, False], size=1, p=[0.2, 0.8])[0]
    

    def __createCustomer(self):

        f = open(self.statesFilePath, 'r')
        # Remove all whitespace characters and split the string into a list of US states
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfCustomers):
            customer = Customer(
                    _,\
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

        f = open(self.statesFilePath, 'r')
        # Remove all whitespace characters and split the string into a list of US states
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfAgents):
            agent = Agent(
                    _,\
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
        writer = pd.ExcelWriter('output/output_results.xlsx', engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        customersDf.to_excel(writer, sheet_name='Customers', index=True)
        agentsDf.to_excel(writer, sheet_name='Agents', index=True)

        # Generate the Reports sheet
        workbook = writer.book
        worksheet = workbook.add_worksheet('Reports')
        writer.sheets['Reports'] = worksheet
        
        customerReportsDf = customersDf['call received']
        customerReportsDf.name = 'Customers'
        customerReportsDf.to_excel(writer, sheet_name='Reports', index=True, start_col=0, start_row=1)

        agentReportsDf = agentsDf[['call received', 'voicemail left']]
        agentReportsDf.name = 'Agents'
        agentReportsDf.to_excel(writer, sheet_name='Reports', index=True, start_col=0, start_row=customerReportsDf.shape[0] + 4)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


def createSimulation(agents, customers, condition):

    # agents = list(self.__createAgent())
    # customers = list(self.__createCustomer())

    # agentWithVoicemails = []

    for customer in customers:
        
        matching_agents = .__match(customer, agents)

        if len(matching_agents) > 1: # if there more than 1 matching agent, randomly select one
            random_number = np.random.randint(low=0, high=len(matching_agents)-1, size=1,dtype=int)[0]
            
            random_timeout = np.random.randint(low=50, high=300, size=1, dtype=int)[0]

            selected_agent = matching_agents[random_number]

            # Increment number of calls this agent receives by 1.
            selected_agent.callReceived += 1
            
            # if the timeout timestamp of the agent is greater than the current time in epoch format 
            # the agent is busy, voicemail will be left.
            if selected_agent.timeoutTimestamp > int(round(time.time() * 1000)):
                print('agent is busy')
                
                # if the agent already had a voicemail, increment number of voicemails and append the new customer into
                # the list of customer that they need to call back.
                selected_agent.voiceMails.append({
                        'customerID': customer.id,
                        'phoneNumber': customer.phoneNumber
                    })
                # agent_had_voicemail = filter(lambda agent: agent.id == selected_agent.id, agents)
                # if agent_had_voicemail:
                
                # else:
                #     selected_agent.voiceMails.append({
                #             'id': customer.id
                #             'phoneNumber': customer.phoneNumber
                #     })
                # selected_agent.voiceMailLeft += 1
                #self.__returnCustomerVoicemail(customer)
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
    #self.__outputResults(customers, agents)


'''
    filter based on two criteria
    1. attribute matches
    2. current timestamp > timeout attribute

    list of available based on attributes
    length of list
    use Random module to generate a random number
    pick that agent
    reset the timeout based on 50 and 300 miliseconds 

    Are the attributes dynamically given as a part of the input for the program or agent is selected if he/she matches
    all the attributes? 
'''


'''
    if an agent is selected, this agent is locked for a random number until they are free again.


    voice mail process. need to watch the list of
    1.  does agent need to return the voicemail right after they become available again?
    2.  is agent busy and not available to receive the call when they are returning the call? and will they have 
        the same random timeout between 50 -300 miliseconds?
    3.  
'''

'''
    brute-force approach:
    voicemail returns
    each time a new customer calls in, check to see if there are any voicemails that need to be returned. 
    When the agent is returning the call, he/she will be busy for 50-300 miliseconds => assign the timeout timestamp 
    if the customer is reached, delete the voicemail. Otherwise, will check back in the next iteration.

    for agent in agent with voicemails:
        pick first one.
        agent.timestamp = timenow + 50 miliseconds
        customerAvailable = random(true, false)
        customer.callreceived += 1
        if customerAvailable = true:
            voicemail -= 1
            customer.pop(index of the customer)
            

    [{
        'agent#': 2,
        voicemailLeft: 2,
        customer: [10, 11]
    },]

'''

'''
    Parallel approach:
    when an agent is picked to serve a customer, that agent is locked for a number of miliseconds.
    a second thread needs to keep track of all agents. If the main thread tries to grab the object while it's locked, a voice
    mail is left.
'''
