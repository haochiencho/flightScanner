from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/add_flight', methods=['POST'])
def add_flight():
    # TODO: update database with flight information
    # username in URL and remaining info in POST request
    username = request.form['username']

    return get_dashboard(username)

def check_flights_for_all_users():
    # TODO: pull all users from DB and check flight for each destination

    # store flight info in DB
    return None

def get_dashboard(username):
    # TODO: look up destinations in DB and display to user

    return render_template('dashboard.html', name=username)

@app.route('/test_client')
def test_client():
    return render_template('test_client.html')
