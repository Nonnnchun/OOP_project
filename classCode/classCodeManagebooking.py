class Controller:
    def __init__(self):
        self.plane_list = []
        self.account_list = []
        self.flightRoute_list = []

    def flight_search(self):
        pass

class Seat:
    def __init__(self, seat_id, seat_type):
        self.seat_id = seat_id
        self.seat_type = seat_type

    def get_available_seat ():
        pass

    def refund_seat():
        pass

class FlightRoute:
    def __init__(self, origin, destination, departure_time, arrive_time):
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrive_time = arrive_time
    def get_available_flight ():
        pass

class Booking:
    def __init__(self, booking_reference, payment, status, flight, passenger_details, promocode_discount, price, luggage):
        self.booking_reference = booking_reference
        self.payment = payment
        self.status = status
        self.flight = flight
        self.passenger_details = passenger_details
        self.promocode_discount = promocode_discount
        self.price = price
        self.luggage = luggage

    def edit_booking(self):
        pass

    def cancel_booking (eslf):
        pass

class Payment:
    def __init__(self, ticket_price, amount):
        self.ticket_price = ticket_price
        self.amount = amount

    def refund_payment ():
        pass

