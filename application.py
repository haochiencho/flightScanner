from flask import Flask
from flask import render_template
from flask import request
from twilio.rest import Client

app = Flask(__name__)

from firebase import firebase

fire_base = firebase.FirebaseApplication('https://flightscanner-baa11.firebaseio.com', authentication=None)

TWILIO_SID = "ACb1491559fcc64c8db360351aa03c5358"
TWILIO_AUTH = "4c326f27de0da951199d6c74df72263e"
TWILIO_NUM = "+16614909538"

@app.route('/add_flight', methods=['POST'])
def add_flight():
    
    # TODO: update database with flight information
    # username in URL and remaining info in POST request
    username = request.form['username']

    user_data = add_flight_departure_destination(username, fire_base)
    fire_base.put('/users', username, user_data)

    return get_dashboard(username)

def add_flight_departure_destination(username, fire_base):
    price = request.form['price']
    starting_airport = request.form['starting_airport']
    destination_airport = request.form['destination_airport']
    departure_date = request.form['departure_date']
    arrival_date = request.form['arrival_date']
    num_passenger = request.form['num_passengers']
    ticket_type = request.form['ticket_type']

    user_data = fire_base.get('/users', username)

    user_data['local_dest'][starting_airport + '-' + destination_airport] = {
            'num_passenger' : num_passenger,
            'departure_date' : departure_date,
            'arrival_date' : arrival_date,
            'ticket_type' : ticket_type,
            'price' : price
        }

    return user_data


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


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "GET":
        return render_template("test_signup.html")
    username = request.form['username']
    password = request.form['password']
    email = request.form['phone_number']

    user_data = {'local_dest' : {}, 'origin' : 'LAX'}

    fire_base.put('/users', username, user_data)
    return "<h1>success</h1>"
    # TODO: Redirect to dashboard after signing up

@app.route('/')
def index():
    return render_template('homepage.html')

def send_text(dest, message):
    client = Client(TWILIO_SID, TWILIO_AUTH)

    message = client.messages.create(
        to=dest,
        from_=TWILIO_NUM,
        body=message)
