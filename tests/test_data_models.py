class TestDataModels:
  def test_customer_class(self, customer):
    assert customer.age == 23
    assert customer.state == 'Texas'
    assert customer.phoneNumber == 8323449783
    assert customer.numberOfKids == 2
    assert customer.numberOfCars == 3
    assert customer.housingStatus == 'rent'
    assert customer.householdIncome == 60000
    assert customer.callReceived == 0

  def test_customer_to_dict(self, customer):
    assert customer.to_dict() == {
            'age': 23, 
            'state': 'Texas',
            'phone number': 8323449783,
            'number of kids': 2, 
            'number of cars': 3, 
            'housing status': 'rent',
            'household income': 60000,
            'call received': 0
        }
  
  def test_agent_class(self, agent):
    assert agent.age == 40
    assert agent.state == 'West Virginia'
    assert agent.housingStatus == 'own'
    assert agent.householdIncome == [40000, 60000]
    assert agent.timeoutTimestamp == 0
    assert agent.callReceived == 0
    assert agent.voiceMailLeft == 0

  def test_agent_to_dict(self, agent):
    assert agent.to_dict() == {
            'age': 40, 
            'state': 'West Virginia',
            'housing status': 'own',
            'household income': [40000, 60000],
            'call received': 0,
            'voicemail left': 0
        }
  
