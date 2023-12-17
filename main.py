# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify, request 
from src.db.createTable import createAccountsTable
from src.db.insertRecord import insertAccount
from src.db.authorize import checkAccount
from src.db.checkGate import checkGateStatus
from config import BARRIER_STATUS_FILE_PATH
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 

# Check connectivity with backend using client
@app.route('/', methods = ['GET'])
def connectionCheck():
    if(request.method == 'GET'): 
        data = True
        return jsonify({'data': data}) 

# Function to create new account
@app.route('/register', methods = ['POST'])
def register():
    if(request.method == 'POST'):
        # Check if account exists
        if createAccountsTable() == -1:
            return jsonify({
                'data': -1,
                'error': 'Could not create accounts table, check connection with server.'
            })
        # Extract data from request
        data = request.json
        # Convert Data into dictionary
        try:
            data = {
                'username': data.get('username'),
                'email': data.get('email'),
                'password': data.get('password')
            }
        except:
            print("Invalid Data.")
            return jsonify({
                'data' : -1,
                'error': 'Invalid data provided.'
            })
        # Insert the record
        if insertAccount(data) == -1:
            return jsonify({
                'data': -1,
                'error': 'Account probably exists.'
            })
        # Return result
        msg = "register function works"
        return jsonify({'data': 1, 'msg': msg})

# Function to check if the account exists or not
@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        # Extract data from request
        try:
            data = {
                'username': data.get('username'),
                'password': data.get('password')
            }
        except:
            print("Invalid data.")
            return jsonify({
                'data': -1,
                'error': 'Invalid data sent.'
            })
        # Check if account exists
        if checkAccount(data)==-1:
            return jsonify({
                'data': -1,
                'error': 'Error while checking credentials.'
            })
        elif checkAccount(data)==0:
            return jsonify({
                'data': 0,
                'msg': 'Invalid login credentials.'
            })
        # Return results
        return jsonify({
            'data': 1,
            'msg': 'Valid login credentials.'
        })


@app.route('/checkBarrier', methods = ['GET'])
def checkBarrier():
    if (request.method == 'GET'):
        status, duration = checkGateStatus()
        duration_min = 0
        if duration!=-1:
            duration_min = int(duration.total_seconds() // 60)
        # duration_sec = int(duration.total_seconds() % 60)
        if (status==1): #open
            return jsonify({
                'data': 1,
                'duration_min': -1,
                # 'duration_sec': duration_sec,
                "msg": "Gate is open."
            })
        else:
            return jsonify({
                'data': 0,
                'duration_min': duration_min,
                # 'duration_sec': duration_sec,
                "msg": "Gate is closed."
            })


@app.route("/openBarrier", methods = ['GET'])
def openBarrier():
    if (request.method == 'GET'):
        with open(BARRIER_STATUS_FILE_PATH, 'w') as file:
            # Read the content of the file
            file.write(str(6))
            return jsonify({
                'data': 1,
                'msg': "Barrier Opened."
            })


@app.route("/closeBarrier", methods = ['GET'])
def closeBarrier():
    if (request.method == 'GET'):
        with open(BARRIER_STATUS_FILE_PATH, 'w') as file:
            # Read the content of the file
            file.write(str(18))
            return jsonify({
                'data': 1,
                'msg': "Barrier Closed."
            })


# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host="0.0.0.0")