from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/add_flight/<username>')

def add_flight(username=None):
    # TODO: update database with flight information
    # username in URL and remaining info in POST request

    return get_dashboard(username)

def check_flights_for_all_users():
    # TODO: pull all users from DB and check flight for each destination
    # store flight info in DB
    return None

def get_dashboard(username):
    # TODO: look up destinations in DB and display to user

    return render_template('dashboard.html', name=username)
