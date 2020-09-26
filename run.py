from flask import Flask, jsonify
from project.callcenter import CallCenter

app = Flask(__name__)


@app.route('/api/v1/run_simulation', methods=['GET','POST'])
def run_simulation():
  noOfCustomers = 1000
  noOfAgents = 20

  newSimulation = CallCenter(noOfCustomers, noOfAgents)
  newSimulation.createSimulation()

  return jsonify({
    "message": "simuation finished running"
  })

if __name__ == '__main__':
  app.run(debug=True)
