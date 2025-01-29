```mermaid

classDiagram

class Flight {
      -origin
      -destination
      -departure_time
      -arrive_time
      -airline
      -seatclass
      -flightType
      -layovers
      +Flightsearch()
}

class SeatClass {
      -name
      -price
      -seat_available
}

class Airport{
      -name
}

class Booking {
      -booking_id
      -user
      -status

}

class Payment {
      -ticket_price
      -type
      -amount
}

class Ticket {
      -ticket_id
      -seatclass
      -passengerType
      -promocode_discount
      -price
      +price_cal()
}

class User {
      -email
      -point
      +login()
      +register()
      +Use_point()
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

class PassengerType{
      -type
      -discount_percent
}

class PerchasedHistory{
      -user
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
PassengerType <|-- Adult
PassengerType <|-- Child
PassengerType <|-- Todler
Payment <|-- OnlineBanking
Payment <|-- Card
Card <|-- Credit_Card
Card <|-- Debit_Card
Flight o-- SeatClass
Flight o-- Airport
Flight o-- FlightType
Flight o-- Booking
Booking <-- Ticket
Ticket <-- Payment
Ticket <-- PassengerType
Ticket <-- Promocode
User <-- PerchasedHistory
User <-- Membership
Promocode -- User