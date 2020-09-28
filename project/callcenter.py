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
        def matchAttr(agent):
            if (agent.age[0] <= customer.age and agent.age[1] >= customer.age) or \
                (agent.householdIncome[0] <= customer.householdIncome and agent.householdIncome[1] >= customer.householdIncome) or \
                customer.state in agent.state:
                return True
            else:
                return False

        return list(filter(lambda agent: matchAttr(agent), agents))
    

    def __createCustomer(self):

        f = open(self.statesFilePath, 'r')
        # Remove all whitespace characters and split the string into a list of US states
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfCustomers):
            customer = Customer(
                    id=_,\
                    age=np.random.randint(ageLow,ageHigh, size=1, dtype=int)[0],\
                    state=self.fake_data.random_element(elements=states),\
                    phoneNumber=self.fake_data.phone_number(),\
                    numberOfKids=self.fake_data.random_digit(),\
                    numberOfCars=self.fake_data.random_digit(),\
                    housingStatus=self.fake_data.random_element(elements=housingStatus),\
                    householdIncome=np.random.randint(incomeLow, incomeHigh, size=1, dtype=int)[0]
                )
            
            yield customer


    def __createAgent(self):

        f = open(self.statesFilePath, 'r')
        states = f.read().replace(' ', '').split(',')
        housingStatus = ('rent', 'own')

        for _ in range(0,self.noOfAgents):
            agent = Agent(
                    id=_,\
                    age=sorted(np.random.randint(ageLow,ageHigh, size=2, dtype=int)),\
                    state=self.fake_data.random_elements(elements=states),\
                    housingStatus=self.fake_data.random_element(elements=housingStatus),\
                    householdIncome=sorted(np.random.randint(incomeLow, incomeHigh, size=2, dtype=int))
                    )
            
            yield agent

    def __returnVoicemail(self, voicemail, agents, customers):
        customerAvailable = np.random.choice([True, False], size=1, p=[0.2, 0.8])[0]
        customer = list(filter(lambda customer: customer.id == voicemail['customerID'], customers))[0]
        agent = list(filter(lambda agent: agent.id == voicemail['agentID'], agents))[0]
        customer.callReceived += 1
        if customerAvailable and agent.timeoutTimestamp < int(round(time.time() * 1000)):
            logging.debug('Agent %s is available to return the voicemail and customer %s is available' %(agent.id, customer.id))
            # If the customer is available to answer the returning phone call,
            # assign new timeout timestamp for this agent as the agent will be busy talking to the customer
            agent.timeoutTimestamp = int(round(time.time() * 1000)) + 50
            logging.debug('Agent %s is now busy talking to the customer' %agent.id)
            return True
        else:
            return False


    def __outputResults(self, customers, agents):
        
        # Prepare customer dataframe for export
        customersDf = pd.DataFrame.from_records([customer.to_dict() for customer in customers])
        customersExport = customersDf.drop(columns=['call received'])

        # Prepare agent dataframe for export
        agentsDf = pd.DataFrame.from_records([agent.to_dict() for agent in agents])
        agentsExport = agentsDf.drop(columns=['call received', 'voicemail left'])

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

        agentReportsDf = agentsDf[['call received', 'voicemail left']]
        agentReportsDf.to_excel(writer, sheet_name='Reports', index=True, index_label='agent_id', startcol=5, startrow=0)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


    def createSimulation(self):

        agents = list(self.__createAgent())
        customers = list(self.__createCustomer())
        voicemails = []

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
                    
                    voicemails.append({
                        'agentID': selected_agent.id,
                        'customerID': customer.id,
                        'phoneNumber': customer.phoneNumber
                    })

                    selected_agent.voicemailLeft += 1

                else:
                # set the timeout of this agent
                    selected_agent.timeoutTimestamp = int(round(time.time() * 1000)) + random_timeout
            
            # Check the voicemail inbox to make sure voice mail is being returned as soon as possible
            logging.debug('Checking and returning voicemails')
            for i, voicemail in enumerate(voicemails, start=0):
                voicemail_returned = self.__returnVoicemail(voicemail, agents, customers)
                if voicemail_returned:
                    voicemails.pop(i)

            # randomly sleep under 30 miliseconds between each calls.
            sleepTime = np.random.randint(low=0, high=30, size=1, dtype=int)[0]
            time.sleep(sleepTime/1000)

        # Make sure that all voice mails are returned and all customers are reached
        logging.debug('Checking voicemails again')
        while len(voicemails) > 0:
            for i, voicemail in enumerate(voicemails, start=0):
                voicemail_returned = self.__returnVoicemail(voicemail, agents, customers)
                if voicemail_returned:
                    voicemails.pop(i)

        # calculate agent utilization
        agentUtilized = list(filter(lambda agent: agent.timeoutTimestamp != 0, agents))
        agentUtilization = len(agentUtilized)/len(agents) * 100
        print('Agent Utilization: %s %%' %agentUtilization)

        #Output the results into an Excel file
        self.__outputResults(customers, agents)
