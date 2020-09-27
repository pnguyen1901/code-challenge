from flask import Flask, jsonify
from project.callcenter import CallCenter
import traceback

app = Flask(__name__)


@app.route('/api/v1/run_simulation', methods=['GET','POST'])
def run_simulation():
  try:
    noOfCustomers = 1000
    noOfAgents = 20

    newSimulation = CallCenter(noOfCustomers, noOfAgents)
    newSimulation.createSimulation()

    return jsonify({
      "message": "simuation finished running"
    })
  except Exception:
    error = traceback.format_exc(limit=None, chain=True)
    
    return jsonify({
      "message": error
    })

if __name__ == '__main__':
  app.run(debug=True)
