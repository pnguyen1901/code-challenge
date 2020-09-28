import pytest
from project.dataModels import Agent

@pytest.fixture
def agent():
  return Agent(
    id=1,
    age=[30,40],
    state=['West Virginia'],
    housingStatus='own',
    householdIncome=[40000, 60000]
  )
