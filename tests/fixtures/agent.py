import pytest
from project.dataModels import Agent

@pytest.fixture
def agent():
  return Agent(
    40,
    'West Virginia',
    'own',
    [40000, 60000],
  )
