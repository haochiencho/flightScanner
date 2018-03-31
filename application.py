from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/add_flight/<name>')

def add_flight(name=None):
    # TODO: update database with flight information
    # username in URL and remaining info in POST request

    return render_template('dashboard.html', name=name)

def check_flights_for_all_users():
    # TODO: pull all users from DB and check flight for each destination
    # store flight info in DB

def get_dashboard(username):
    # TODO: look up destinations in DB and display to user
