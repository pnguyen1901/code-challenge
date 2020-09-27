from flask import Flask, jsonify, request
from project.callcenter import CallCenter
import traceback

app = Flask(__name__)

@app.route('/api/v1/run_simulation', methods=['POST'])
def run_simulation():
  try:
    noOfCustomers = int(request.form.get('noOfCustomers', default=1000))
    noOfAgents = int(request.form.get('noOfAgents', default=20))

    newSimulation = CallCenter(noOfCustomers, noOfAgents)
    newSimulation.createSimulation()

    return jsonify({
      "message": "simulation finished running"
    })
  except Exception:
    error = traceback.format_exc(limit=None, chain=True)
    
    return jsonify({
      "message": error
    }), 500

if __name__ == '__main__':
  app.run(debug=True)
