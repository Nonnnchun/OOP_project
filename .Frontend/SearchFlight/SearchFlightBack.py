from fasthtml.common import *
from hmac import compare_digest
from random import randint, choice
from datetime import datetime, timedelta

# ================================
#   ACCOUNT MANAGEMENT CLASSES
# ================================

# Controller to manage users
class Controller:
   def __init__(self):
      self.accounts = []  # List of registered accounts
      self.logged_in_user = None  # Store currently logged-in user
      self.flights = []  # List of flights
      self._next_flight_id = 1  # Track flight IDs

   def register(self, email, password, firstname, lastname):
      if any(acc.email == email for acc in self.accounts):
         return "Email already registered!"
      
      user_detail = UserDetail(firstname, lastname)
      new_account = Account(email, password, user_detail)
      self.accounts.append(new_account)
      return "Registration successful!"

   def login(self, email, password):
      for acc in self.accounts:
         if acc.email == email and acc.check_password(password):
               self.logged_in_user = acc
               return "Login successful!"
      return "Invalid email or password!"

   def get_logged_in_user(self):
      return self.logged_in_user

   def logout(self):
      self.logged_in_user = None

   def search_flights(self, origin, destination, date):
      # This method will search for flights based on the origin, destination, and date
      # For simplicity, let's assume we have a list of flights stored in self.flights
      results = [flight for flight in self.flights if flight.origin == origin and flight.destination == destination and flight.date == date]
      return results

   def add_flight(self, flight):
      flight.id = self._next_flight_id
      self._next_flight_id += 1
      self.flights.append(flight)
      return flight

   def get_flight(self, flight_id):
      return next((flight for flight in self.flights if flight.id == flight_id), None)

   def update_flight(self, updated_flight):
      for i, flight in enumerate(self.flights):
         if flight.id == updated_flight.id:
               self.flights[i] = updated_flight
               return updated_flight
      return None

   def delete_flight(self, flight_id):
      self.flights = [flight for flight in self.flights if flight.id != flight_id]
   
   def filter_flights(self, query=None, available_only=False):
      filtered = self.flights
      if query:
         query = query.lower()
         filtered = [flight for flight in filtered 
                  if query in flight.origin.lower() or 
                     query in flight.destination.lower()]
      if available_only:
         filtered = [flight for flight in filtered if flight.available]

      return filtered

class UserDetail:
   def __init__(self, firstname, lastname, points=0):
      self.firstname = firstname
      self.lastname = lastname
      self.points = points

class Account:
   def __init__(self, email, password, userdetail):
      self.email = email
      self.password = password
      self.userdetail = userdetail

   def check_password(self, password):
      return compare_digest(self.password, password)

class FlightRoute:
   def __init__(self, id, origin, destination, date, price, available=True):
      self.id = id
      self.origin = origin
      self.destination = destination
      self.date = date
      self.price = price
      self.available = available

controller = Controller()
locations = ["Bangkok", "Chiang Mai", "Phuket", "Hat Yai"]
flights_to_add = []

for i in range(1, 10000):  
   origin = choice(locations)
   destination = choice([loc for loc in locations if loc != origin])  # Ensure destination is different
   random_days = randint(1, 30)  # Pick a random date within the next 300 days
   flight_date = (datetime(2025, 3, 1) + timedelta(days=random_days)).strftime("%Y-%m-%d")
   price = randint(3000, 15000)  # Random price between 3,000 and 15,000 THB
   available = choice([True])  # Random availability

   flights_to_add.append(FlightRoute(i, origin, destination, flight_date, price, available))

# Add flights to the controller
for flight in flights_to_add:
   controller.add_flight(flight)

tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

controller.add_flight(FlightRoute(100000, "Bangkok", "Chiang Mai", "2025-03-09", 6500, True))
controller.add_flight(FlightRoute(1000001, "Chiang Mai", "Bangkok", tomorrow, 7000, True))