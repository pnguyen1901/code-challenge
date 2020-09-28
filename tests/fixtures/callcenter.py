import pytest
from project.callcenter import CallCenter
import os
from dotenv import load_dotenv
load_dotenv()

# Load env var
testCustomerSize = int(os.getenv('testCustomerSize'))
testAgentSize = int(os.getenv('testAgentSize'))

@pytest.fixture
def callcenter():
  return CallCenter(testCustomerSize, testAgentSize)