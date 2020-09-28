import pytest
from project.dataModels import Customer

@pytest.fixture
def customer():
  return Customer(
    23,
    'Texas',
    8323449783,
    2,
    3,
    'rent',
    60000
  )