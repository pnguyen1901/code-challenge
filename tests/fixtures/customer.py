import pytest
from project.dataModels import Customer

@pytest.fixture
def customer():
  return Customer(
    id=1,
    age=23,
    state='Texas',
    phoneNumber=8323449783,
    numberOfKids=2,
    numberOfCars=3,
    housingStatus='rent',
    householdIncome=60000
  )