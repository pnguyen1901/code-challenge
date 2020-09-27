from .dataModels import Agent, Customer
import time
import numpy as np
from faker import Faker
from functools import reduce
import pandas as pd
import logging, threading
from dotenv import load_dotenv
import os
load_dotenv()

ageLow = int(os.getenv('age_low'))
ageHigh = int(os.getenv('age_high'))
incomeLow = int(os.getenv('income_low'))
incomeHigh = int(os.getenv('income_high'))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-9s) %(message)s',)

class CallCenter:

    def __init__ (self, noOfCustomers, noOfAgents):
        self.noOfCustomers = noOfCustomers
        self.noOfAgents = noOfAgents
        self.fake_data = Faker()
        self.statesFilePath = 'assets/listOf50States.txt'

    @staticmethod
    def __match(customer, agents):

        return list(filter(lambda agent: agent.age[0] <= customer.age and agent.age[1] >= customer.age, agents))
    

    def __createCustomer(self):

        f = open(self.statesFilePath, 'r')
        # Remove all whitespace characters and split the string into a list of US states
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfCustomers):
            customer = Customer(
                    _,\
                    np.random.randint(ageLow,ageHigh, size=1, dtype=int)[0],\
                    self.fake_data.random_element(elements=states),\
                    self.fake_data.phone_number(),\
                    self.fake_data.random_digit(),\
                    self.fake_data.random_digit(),\
                    self.fake_data.random_element(elements=housingStatus),\
                    np.random.randint(incomeLow, incomeHigh, size=1, dtype=int)[0]
                )
            
            yield customer


    def __createAgent(self):

        f = open(self.statesFilePath, 'r')
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfAgents):
            agent = Agent(
                    _,\
                    sorted(np.random.randint(ageLow,ageHigh, size=2, dtype=int)),\
                    self.fake_data.random_elements(elements=states),\
                    self.fake_data.random_element(elements=housingStatus),\
                    sorted(np.random.randint(incomeLow, incomeHigh, size=2, dtype=int))
                    )
            
            yield agent

    def returnVoicemail(self, agent, customers, condition):
        with condition:
            logging.debug('waiting to return customer call')
            condition.wait()
            while len(agent.voiceMails) > 0:
                logging.debug('returning customer call')
                customerAvailable = np.random.choice([True, False], size=1, p=[0.2, 0.8])[0]
                customer = list(filter(lambda customer: customer.id == agent.voiceMails[0]['customerID'], customers))[0]
                customer.callReceived += 1
                if customerAvailable:
                    agent.voiceMails.pop(0)
                    logging.debug('customer is available. Agent is now busy talking to the customer')
                    # If the customer is available to answer the returning phone call,
                    # assign new timeout timestamp for this agent as the agent will be busy talking to the customer
                    agent.timeoutTimestamp = int(round(time.time() * 1000)) + 50

    @staticmethod
    def serveCustomer(agent, timeout, condition):
        '''
            timeout is a random number between 50 - 300.
        '''
        logging.debug('Agent is busy serving customer')
        with condition:
            time.sleep(timeout/1000) # convert to miliseconds.
            logging.debug('Agent is available now')
            condition.notify()

    def __outputResults(self, customers, agents):
        
        # Prepare customer dataframe for export
        customersDf = pd.DataFrame.from_records([customer.to_dict() for customer in customers])
        customersExport = customersDf.drop(columns=['call received'])

        # Prepare agent dataframe for export
        agentsDf = pd.DataFrame.from_records([agent.to_dict() for agent in agents])
        agentsExport = agentsDf.drop(columns=['call received', 'voicemail left', 'voicemails'])

        # Create a Pandas Excel writer using Xlsxwriter as the engine.
        writer = pd.ExcelWriter('output/output_results.xlsx', engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        customersExport.to_excel(writer, sheet_name='Customers', index=False)
        agentsExport.to_excel(writer, sheet_name='Agents', index=False)

        # Generate the Reports sheet
        workbook = writer.book
        worksheet = workbook.add_worksheet('Reports')
        writer.sheets['Reports'] = worksheet
        
        customerReportsDf = customersDf['call received']
        customerReportsDf.to_excel(writer, sheet_name='Reports', index=True, index_label='customer_id', startcol=0, startrow=0)

        agentReportsDf = agentsDf[['call received', 'voicemail left', 'voicemails']]
        print(customerReportsDf.shape)
        agentReportsDf.to_excel(writer, sheet_name='Reports', index=True, index_label='agent_id', startcol=5, startrow=0)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


    def createSimulation(self):

        agents = list(self.__createAgent())
        customers = list(self.__createCustomer())

        # agentWithVoicemails = []

        for customer in customers:
            
            matching_agents = self.__match(customer, agents)

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
                    
                    # Increment the number of voicemail left for this agent by 1 and append the new customer into
                    # the list of customer that they need to call back.
                    selected_agent.voiceMails.append({
                            'customerID': customer.id,
                            'phoneNumber': customer.phoneNumber
                        })
                    
                    selected_agent.voicemailLeft += 1

                    # setup a new thread to watch for the agent timeout and return customer's call once the agent becomes available again.
                    condition = threading.Condition()
                    cs = threading.Thread(target=self.returnVoicemail, args=(selected_agent, customers, condition,))
                    pd = threading.Thread(target=self.serveCustomer, args=(selected_agent, random_timeout, condition,))

                    cs.start()
                    time.sleep(1/1000)
                    pd.start()
                    
                    cs.join()
                    pd.join()

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

        #Output the results into an Excel file
        self.__outputResults(customers, agents)
