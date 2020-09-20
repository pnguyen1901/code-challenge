from mockData import create_customer, Agent
import time
import numpy as np


customers = create_customer()

f = open('listOf50States.txt', 'r')
states = f.read().replace(' ','').split(',')

agents = [
    {
        'id': 1,
        'age': [18,30],
        'state': states[:10],
        'timestamp': 0
    },
    {
        'id': 2,
        'age': [31,50],
        'state': states[11:30],
        'timestamp': 0
    },
    {
        'id': 3,
        'age': [31,50],
        'state': states[11:30],
        'timestamp': 0
    },
    {
        'id': 4,
        'age': [51,70],
        'state': states[31:40],
        'timestamp': 0
    },
    {
        'id': 5,
        'age': [51,70],
        'state': states[31:40],
        'timestamp': 0
    },
    {
        'id': 6,
        'age': [71,90],
        'state': states[41:50],
        'timestamp': 0
    }
]

def match(customer, agents):

    return list(filter(lambda agent: agent['age'][0] <= customer.age and agent['age'][1] >= customer.age, agents))


def call_center(customers, agents):

    call_back_customers = []

    for _ in range(19):
        current_customer = next(customers)
        matching_agents = match(current_customer, agents)
        #print(matching_agents)
        
        if len(matching_agents) > 1: # if there more than 1 matching agent, randomly select one
            random_number = np.random.randint(low=0, high=len(matching_agents)-1, size=1,dtype=int)[0]
            
            random_timeout = np.random.randint(low=50, high=300, size=1, dtype=int)[0]
            print(random_timeout)
            selected_agent = matching_agents[random_number]
            # if the current timestamp of the agent is less than timestamp now in epoch format, the agent 
            if selected_agent['timestamp'] < int(round(time.time() * 1000)) and selected_agent['timestamp'] > 0:
                print('agent is busy')
                call_back_customers.append(current_customer)
            else:
            # set the timeout of this agent
                selected_agent['timestamp'] = int(round(time.time() * 1000)) + random_timeout

    print(call_back_customers)


call_center(customers, agents)


# Get a list of agents filtered by the attributes
# available_list = filter(lambda agent: agents['state'] == , agents)

# The function needs to 

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