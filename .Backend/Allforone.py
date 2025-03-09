class Controller:
    def __init__(self):
        self.plane_list = []
        self.account_list = []
        self.flightRoute_list = []
        self.is_logged_in = False
        self.booking_list = []
    
    def turn_into_system(self, user):
        if not user.has_account():
            self.account.register()
            if self.account.is_success():
                print("Register successful")
            return self.auto_path_to_login(user)
        else:
            self.account.login()
            if self.account.is_correct():
                print("Login successful")
                self.is_logged_in = True
                self.display_home_page()

    def auto_path_to_login(self, user):
        self.account.login()
        if self.account.is_correct():
            print("Login successful")
            self.is_logged_in = True
            self.display_home_page()

    def display_home_page(self):
        print("Displaying home page")

    def flight_search(self):
        pass

class Seat:
    def __init__(self, seat_id, seat_type):
        self.seat_id = seat_id
        self.seat_type = seat_type
        self.seat_status = True

    def update_seat_status(self):
        self.seat_status = False

class Airport:
    def __init__(self, name):
        self.name = name

class Plane:
    def __init__(self, plane_id, aircraft, seats):
        self.plane_id = plane_id
        self.aircraft = aircraft
        self.seats = seats

class FlightRoute:
    def __init__(self, origin, destination, departure_time, arrive_time):
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrive_time = arrive_time

    def display_flight_results(self):
        print("Display flight results")

class Booking:
    def __init__(self, booking_reference, status, flight, promocode_discount, price, luggage, seat):

        self.booking_reference = booking_reference
        self.status = False
        self.flight = flight
        self.passenger_details = []
        self.promocode_discount = promocode_discount
        self.price = price
        self.luggage = luggage
        self.pay_by = None
        self.seat = []


    def edit_booking(self):
        pass

    def price_cal(self):
        pass

    def update_booking_status(self):
        self.status = True

    def create_pay_by(self, method_id):
        self.pay_by = self.method_id

class Luggage:
    def __init__(self, kilogram, price_rate):
        self.kilogram = kilogram
        self.price_rate = price_rate

class Payment:
    def __init__(self, price, booking_reference):
        self.price = price
        self.booking_reference = booking_reference

    def process_payment(self, payment_method, booking_reference):
        return payment_method.pay(booking_reference)

class PaymentMethod:
    def __init__(self, method_id):
        self.method_id = method_id

    def pay(self, booking_reference):
        booking = controller.booking_search(booking_reference)

        booking.create_pay_by(self.method_id)
        booking.update_booking_status()
        seat_list = booking.seat
        for seat in seat_list:
            seat.update_seat_status()

class OnlineBanking(PaymentMethod):
    def __init__(self, method_id="OnlineBanking"):
        super().__init__(method_id)

class Card(PaymentMethod):
    def __init__(self, method_id, card_number, card_CVV, card_EXP):
        super().__init__(method_id)
        self.card_number = card_number
        self.card_CVV = card_CVV
        self.card_EXP = card_EXP

class CreditCard(Card):
    def __init__(self, method_id, card_number, card_CVV, card_EXP):
        super().__init__("CreditCard", card_number, card_CVV, card_EXP)

class DebitCard(Card):
    def __init__(self, method_id, card_number, card_CVV, card_EXP):
        super().__init__("DebitCard", card_number, card_CVV, card_EXP)

class Account:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.purchased_history = []
        self.userdetail = None

    def login(self):
        print("Login Page")
        pass
        # Implement login logic
    
    def register(self, email, password, userdetail):
        print("Registering user")
        self.email = email
        self.password = password
        self.userdetail = userdetail
        # Implement registration logic
    
    def forgotpass(self):
        print("Forgot Password Page")
        pass
        # Implement forgot password logic
    
    def is_correct(self):
        # Implement validation
        return True
    
    def is_success(self):
        # Check if registration was successful
        return True
    
    def return_home_page(self):
        print("Returning Home Page")
        pass

    def get_booking_list(self):
        return []

    def get_promocode(self):
        return self.user_detail.get_promocode()

    def use_points(self, points):
        if self.user_detail.point >= points:
            self.user_detail.point -= points
            return True
        return False

    def change_password(self, old_password, new_password):
        if self.password == old_password:
            self.password = new_password
            return True
        return False

    def logout(self):
        pass


class UserDetail:
    def __init__(self, firstname, lastname, birthday, gender, identification, nationality, phone_number, address, point, promocode_list):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.gender = gender
        self.identification = identification
        self.nationality = nationality
        self.phone_number = phone_number
        self.address = address
        self.point = point
        self.promocode_list = []

    def editprofile(self, firstname=None, lastname=None, birthday=None, gender=None, identification=None, nationality=None, phone_number=None, address=None, point=None):
        if firstname: self.firstname = firstname
        if lastname: self.lastname = lastname
        if birthday: self.birthday = birthday
        if gender: self.gender = gender
        if identification: self.identification = identification
        if nationality: self.nationality = nationality
        if phone_number: self.phone_number = phone_number
        if address: self.address = address

    def calculate_points(self, transactions):
        total_points = 0
        for transaction in transactions:
            total_points += transaction['amount'] * 0.1  # Assuming 10% of transaction amount is converted to points
        self.point += total_points
        return total_points
        
    def usepoint(self, points):
        if self.point >= points:
            self.point -= points
            return True
        return False

    def get_promocode(self):
        return self.promocode_list

class Promocode:
    def __init__(self, code, discount_percent, expiration_date):
        self.code = code
        self.discount_percent = discount_percent
        self.expiration_date = expiration_date

    def is_valid(self):
        return True

class PassengerDetail:
    def __init__(self, passengerType, seat):
        self.passengerType = passengerType
        self.nametitle = None
        self.name = None
        self.surname = None
        self.day_bday = None
        self.month_bday = None
        self.year_bday = None
        self.email = None
        self.phone_number = None
        self.phone_number = seat

    def update_passenger_details(self, nametitle, name, surname, day_bday, month_bday, year_bday, email, phone_number):
        self.nametitle = nametitle
        self.name = name
        self.surname = surname
        self.day_bday = day_bday
        self.month_bday = month_bday
        self.year_bday = year_bday
        self.email = email
        self.phone_number = phone_number
        
class PassengerType:
    def __init__(self, type, discount_percent):
        self.type = type
        self.discount_percent = discount_percent

# Mockup Data
def generate_seats(rows, seat_prefix):
    return [Seat(f"{seat_prefix}{str(row).zfill(2)}", seat_prefix) for row in range(1, rows + 1)]

seats_flight1_list = (
    generate_seats(20, "EC") + 
    generate_seats(5, "BS") +   
    generate_seats(2, "FC")    
)
plane1 = Plane("P001", "Boeing 737", seats_flight1_list)
flight1 = FlightRoute("JFK", "LAX", "10:00", "13:00")

promocode1 = Promocode("DISCOUNT10", 10, "2025-12-31")
promocode2 = Promocode("SALE20", 20, "2025-06-30")
user_detail1 = UserDetail("John", "Doe", "1990-05-15", "Male", "123456789", "USA", "555-1234", "123 Main St", 100, [promocode1, promocode2])
account1 = Account("password123", "john.doe@example.com")
controller = Controller()
controller.account_list.append(account1)