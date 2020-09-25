import pytest
from project.callcenter import CallCenter

@pytest.fixture
def callcenter():
  return CallCenter(500, 10)