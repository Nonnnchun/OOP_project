from fasthtml.common import *
from hmac import compare_digest
from random import randint, choice
from datetime import datetime, timedelta

# ================================
#   ACCOUNT MANAGEMENT CLASSES
# ================================
class UserDetail:
   def __init__(self, firstname, lastname, points=0):
        # birthday, gender, identification, nationality, phone_number, address,
        self.__firstname = firstname
        self.__lastname = lastname
        self.__points = points
        self.__birthday = []
        self.__gender = []
        self.__identification = []
        self.__nationality = []
        self.__phone_number = []
        self.__address = []
        self.__promocode_list = []
   
   @property
   def firstname(self):
      return self.__firstname
   @property
   def lastname(self):
      return self.__lastname
   @property
   def points(self):
      return self.__points
   @property
   def birthday(self):
      return self.__birthday
   @property
   def gender(self):
      return self.__gender
   @property
   def identification(self):
      return self.__identification
   @property
   def nationality(self):
      return self.__nationality
   @property
   def phone_number(self):
      return self.__phone_number
   @property
   def address(self):
      return self.__address
   @property
   def promocode_list(self):
      return self.__promocode_list
   
   @lastname.setter
   def lastname(self, new_lastname):
      self.__lastname = new_lastname

   @phone_number.setter
   def phone_number(self, new_number):
      self.__phone_number = new_number

   @address.setter
   def address(self, address):
      self.__address = address
        
   def edit_profile(self, firstname=None, lastname=None, phone_number=None, address=None):
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if phone_number:
            self.phone_number = phone_number
        if address:
            self.address = address

class Account:
   def __init__(self, email, password, userdetail):
      self.__email = email
      self.__password = password
      self.__userdetail = userdetail

   @property
   def email(self):
      return self.__email
   @property
   def password(self):
      return self.__password
   @property
   def userdetail(self):
      return self.__userdetail
   
   @password.setter
   def password(self, new_password):
      self.__password = new_password
      
   def check_password(self, password):
      return compare_digest(self.password, password)
   
   def change_password(self, old_password, new_password, confirm_new_password):
    if old_password != self.password:
        return "Old password is incorrect"
    if new_password != confirm_new_password:
        return "New passwords do not match"
    if len(new_password) < 6:  # Ensure new password is strong
        return "New password must be at least 6 characters long"
    if new_password == old_password:  # Ensure new password is different from the old one
        return "New password cannot be the same as the old password"

    self.password = new_password
    return "Password changed successfully"

# Controller to manage users
class Controller:
   def __init__(self):
      self.__accounts = []  # List of registered accounts
      self.__logged_in_user = None  # Store currently logged-in user
      self.__flights = []  # List of flights
      self._next_flight_id = 1  # Track flight IDs
   
   @property
   def accounts(self):
      return self.__accounts
   @property
   def logged_in_user(self):
      return self.__logged_in_user
   @property
   def flights(self):
      return self.__flights
   
   @logged_in_user.setter
   def logged_in_user(self, user):
      self.__logged_in_user = user
   
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

class FlightRoute:
   def __init__(self, id, origin, destination, date, price, available=True):
      self.__id = id
      self.__origin = origin
      self.__destination = destination
      self.__date = date
      self.__price = price
      self.__available = available

   @property
   def id(self):
      return self.__id
   @property
   def origin(self):
      return self.__origin
   @property
   def destination(self):
      return self.__destination
   @property
   def date(self):
      return self.__date
   @property
   def price(self):
      return self.__price
   @property
   def available(self):
      return self.__available
   
   @id.setter
   def id(self, new_id):
      self.__id = new_id
      
   @available.setter
   def available(self, is_available):
      self.__available = is_available
   
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
