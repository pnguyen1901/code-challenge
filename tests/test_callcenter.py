import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Load env var
testCustomerSize = int(os.getenv('testCustomerSize'))
testAgentSize = int(os.getenv('testAgentSize'))

class TestCallCenter:
  
  def test_create_customer(self, callcenter):
    '''
      test flow
      2. make sure to delete if there is output_results.xlsx file in output folder.
      3. make sure there are 3 worksheets. Customers, Agents, Reports.
      4. There is a table in Customers with the shape that we expected. Matching number of customers expected to be created, with the right set
      of column names
      repeat the same for the rest.
    '''
    output_filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output/output_results.xlsx')
    # Step 1: If there is already an output file, first delete it.
    if os.path.exists(output_filepath):
      os.remove(output_filepath)
    
    # Step 2: Test if the simulation actually created a new output_results.xlsx
    callcenter.createSimulation()
    assert os.path.exists(output_filepath) == True

    # Step 3: Test if the workbook has the following sheets: Customers, Agents, Reports
    outputExcelFile = pd.ExcelFile(output_filepath)
    sheetNames = outputExcelFile.sheet_names
    assert sheetNames == ['Customers', 'Agents', 'Reports']

    # Step 4: Test if the data in these sheets have the format that we are expecting them to be.
    # Check Customers sheet
    CustomerDf = pd.read_excel(outputExcelFile, 'Customers')
    assert CustomerDf.shape == (testCustomerSize, 8)
    columnHeaders = list(CustomerDf.columns)
    assert columnHeaders == ['id', 'age', 'state',\
      'phone number','number of kids', 'number of cars',\
      'housing status','household income']

    # Check Agents sheet
    AgentDf = pd.read_excel(outputExcelFile, 'Agents')
    assert AgentDf.shape == (testAgentSize, 5)
    columnHeaders = list(AgentDf.columns)
    assert columnHeaders == ['id', 'age', 'state', 'housing status','household income']

    # Check Reports sheet
    CustomerReportDf = outputExcelFile.parse(sheet_name='Reports', usecols="A:B")
    assert CustomerReportDf.shape == (testCustomerSize, 2)

    AgentReportDf = outputExcelFile.parse(sheet_name='Reports', skipfooter=testCustomerSize-testAgentSize, usecols="F:H")
    assert AgentReportDf.shape == (testAgentSize, 3)


