from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)
from firebase import firebase
fire_base = firebase.FirebaseApplication('https://flightscanner-baa11.firebaseio.com', authentication=None)

@app.route('/add_flight', methods=['POST'])
def add_flight():
    username = request.form['username']

    user_data = add_flight_departure_destination(username)
    fire_base.put('/users', username, user_data)

    return get_dashboard(username)

def add_flight_departure_destination(username):
    price = request.form['price']
    starting_airport = request.form['starting_airport']
    destination_airport = request.form['destination_airport']
    departure_date = request.form['departure_date']
    arrival_date = request.form['arrival_date']
    num_passenger = request.form['num_passengers']
    ticket_type = request.form['ticket_type']

    user_data = fire_base.get('/users', username)

    if 'local_dest' not in user_data:
        user_data['local_dest'] = {}

    user_data['local_dest'][starting_airport + '-' + destination_airport] = {
            'num_passenger' : num_passenger,
            'departure_date' : departure_date,
            'arrival_date' : arrival_date,
            'ticket_type' : ticket_type,
            'price' : price
        }

    return user_data

@app.route('/test_check_flights')
def check_flights_for_all_users():
    # TODO: pull all users from DB and check flight for each destination
    # store flight info in DB

    users_data = fire_base.get('/users', None)
    print(users_data)
    if users_data != None:
        for username in users_data:
            user_data = users_data[username]

    return render_template('homepage.html')

def get_dashboard(username):
    # TODO: look up destinations in DB and display to user

    return render_template('dashboard.html', name=username)

@app.route('/add_flight_test_client')
def add_flight_test_client():
    return render_template('test_client.html')

@app.route('/')
def index():
    return render_template('homepage.html')
