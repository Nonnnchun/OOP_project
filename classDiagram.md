```mermaid

classDiagram

class Flight {
      -origin
      -destination
      -departure_time
      -arrive_time

      -PLane
      -flightType
      -layovers
      +Flightsearch()
      +Flightfilter()
}

class SeatClass {
      -name
      -price
      -seat_available
}

class Airport{
      -name
}
class Plane{
      -plane_id
      -aircraft
      -seatclass

}

class Booking {
      -booking_reference
      -payment
      -status
      -flight
      -passengerDetail list
      -promocode_discount
      -price
      +editBooking()
      +price_cal()
}

class Payment {
      -ticket_price
      -amount
      +processPayment()
}

class User {
      -email
      -point
      -PurchesedHistory
      +login()
      +register()
      +Usepoint()
}

class Promocode{
      -code
      -discount_percent
      -expiration_date
      +IsValid()
}

class FlightType{
      -name
}

class PassengerDetail{
      -paassengerType
      -passengerName
      -contact
      -Birthday
}

class PassengerType{
      -type
      -discount_percent
}

class PurchasedHistory{
      -booking
}

class Membership{
      -user
      -discount_percent
}

SeatClass <|-- BusinessClass
SeatClass <|-- EconClass
SeatClass <|-- FirstClass
SeatClass <|-- PremiumEconClass
FlightType <|-- DirectFlight
FlightType <|-- OneStop
FlightType <|-- TwoStop
PassengerDetail --> PassengerType
Payment <|-- OnlineBanking
Payment <|-- Card
Card <|-- Credit_Card
Card <|-- Debit_Card
Flight o-- Airport 
Plane o-- SeatClass
Flight o-- FlightType
Flight "1" o-- "*" Booking
Booking --> Payment
Booking <-- SeatClass
Booking --> PassengerDetail
Booking --> Promocode
User "1" <-- "*" Booking
User --> PurchasedHistory
User <-- Membership
Promocode -- User
PurchasedHistory <-- Booking
Flight o-- Plane
Plane <-- SeatClass