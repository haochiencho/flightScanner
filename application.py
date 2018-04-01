from flask import Flask, render_template, request, abort
from twilio.rest import Client
import string
import urllib
from random import *
import json
import requests

app = Flask(__name__)

from firebase import firebase
fire_base = firebase.FirebaseApplication('https://flightscanner-baa11.firebaseio.com', authentication=None)

TWILIO_SID = "ACb1491559fcc64c8db360351aa03c5358"
TWILIO_AUTH = "4c326f27de0da951199d6c74df72263e"
TWILIO_NUM = "16614909538"
airlines = ['united', 'delta', 'southwest', 'alaskaAirline']

print("Opening file . . .")

codeToAirport = {}
file = open("airlines.dat", 'r')
for line in file:
    line = line.replace('"', '')
    args = line.split(',')
    if len(args[4]) != 3:
        continue
    codeToAirport[args[4]] = args[1]

file.close()
print("All airlines loaded")

@app.route('/add_flight', methods=['POST'])
def add_flight():
    username = request.form['username']
    if username == '':
        username = 'bob'

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
    users_data = fire_base.get('/users', None)
    if users_data != None:
        for username in users_data:
            user_data = users_data[username]
            for location_destination in user_data['local_dest']:
                user_flight_info = user_data['local_dest'][location_destination]

                departing_airport, destination_airport = parse_location_destination(location_destination)

                price, airline = get_flight_info(departing_airport, destination_airport,\
                user_flight_info['departure_date'], user_flight_info['arrival_date'])

                price = round(price * float(user_flight_info['num_passenger']), 2)

                sms_message = "Found flight from " + departing_airport + " to " + destination_airport \
                    + " at $" + str(price) + " for " + user_flight_info['num_passenger'] + " passengers! " \
                    + "Please book tickets on www." + str.lower(airline) + ".com"

                user_phone_number = user_data['phone_number']
                send_text(user_phone_number, sms_message)

    return render_template('homepage.html')

def parse_location_destination(location_destination):
    location_arr = location_destination.split('-')
    return location_arr[0], location_arr[1]

def get_flight_info(departure, destination, departure_date, arrival_date):
    # lowest price

    #YYYY-MM-DD
    #https://www.justfly.com/flight/search?campaign=10392&seg0_date=2018-04-28&seg0_time=&seg0_from=LAX&seg0_to=SMF&seg1_date=2018-05-06&seg1_time=&seg1_from=SMF&seg1_to=LAX&num_segments=2&num_adults=1&num_children=0&num_infants=0&preferred_carrier_code=&seat_class=&nearby_airports=0&flexible_date=0&no_penalties=0&non_stop=0

    # url = "https://www.justfly.com/flight/search?campaign=10392&seg0_date=" + departure_date + "&seg0_time=&seg0_from=" + departure + "&seg0_to=" + destination + "seg1_date=" + arrival_date + "&seg1_time=&seg1_from=" + destination + "&seg1_to=" + departure + "&num_segments=2&num_adults=1&num_children=0&num_infants=0&preferred_carrier_code=&seat_class=&nearby_airports=0&flexible_date=0&no_penalties=0&non_stop=0"

    # print(url)

    # page = urllib.request.urlopen(url).read()
    # soup = BeautifulSoup(page, "html.parser")
    #
    # items = soup.findAll("div", {"class": "Flights-Results-FlightResultsList"})
    # print(items)
    #
    # print(soup.prettify())
    #
    # for item in soup.findAll("li", {"class": "fly-itinerary"}):
    #     print('hi')
    #     print(item)

    x = randint(0, 4)
    price = fire_base.get('/flights', departure + '-' + destination)

    airline = airlines[x]

    return price, airline

@app.route("/dash/<username>")
def dash(username=None):
    return get_dashboard(username)

def get_dashboard(username):
    # TODO: look up destinations in DB and display to user
    users_data = fire_base.get('/users', None)
    if users_data != None and username in users_data:
        user = users_data[username]
        flights = []
        print(user)
        if 'local_dest' not in user:
            return render_template('dashboard.html', username=username)
        for key in user['local_dest']:
            flight = user['local_dest'][key]
            departure, destination = key.split('-')
            flight['departure'] = departure
            flight['destination'] = destination
            flights.append(flight)
    else:
        print("Error: User not found")
        abort(500)
    return render_template('dashboard.html', flights=flights, username=username)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "GET":
        return render_template("test_signup.html")
    username = request.form['username']
    password = request.form['password']
    phone_number = request.form['phone_number']
    phone_number = format_phone(phone_number)

    user_data = {'local_dest' : {}, 'origin' : 'LAX', 'phone_number' : phone_number}
    fire_base.put('/users', username, user_data)
    return get_dashboard(username)

def format_phone(phone_number):
    phone_number = phone_number.replace('-', "").replace(' ', "").replace('(', "").replace(')', "")
    for c in phone_number:
        if not c.isdigit():
            abort(400) # Abort with bad request error cod
    if len(phone_number) != 10:
        abort(400)
    phone_number = '+1' + phone_number
    return phone_number

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    print(request.form)
    username = request.form['username']
    print(username)
    return get_dashboard(username)

def send_text(dest, message):
    client = Client(TWILIO_SID, TWILIO_AUTH)

    message = client.messages.create(
        to=dest,
        from_=TWILIO_NUM,
        body=message)
