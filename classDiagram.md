```mermaid

classDiagram
    direction TB
    class Controller {
        -plane
        -account_list
        -flightRoute_list
        +flightsearch()
    }

    class Seat {
        -seat_id
        -seat_type
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
        -luggage
        +editBooking()
        +price_cal()
    }

    class luggage{
        -kilogram
        -price_rate
    }

    class Payment {
        -ticket_price
        -amount
        +processPayment()
    }

    class Account {
        -password
        -email
        -PurchesedHistory
        -Userdetail
        +login()
        +register()
        +forgotpass()

    }
    class Userdetail{
        -Firstname
        -Lastname
        -birthday
        -gender
        -identification
        -nationality
        -phone_number
        -address
        -point
        +editprofile()
        +usepoint()
    }
    class Paymentmethod{

    }

    class Promocode{
        -code
        -discount_percent
        -expiration_date
        +isValid()
    }

    class FlightRoute{
        -origin
        -destination
        -departure_time
        -arrive_time
    }

    class PassengerDetail{
        -paassengerType
        -passengerName
        -contact
        -birthday
    }

    class PassengerType{
        -type
        -discount_percent
    }


 
    PassengerDetail --> PassengerType
    Paymentmethod <|-- OnlineBanking
    Paymentmethod  Payment
    Paymentmethod <|-- Card
    Card <|-- Credit_Card
    Card <|-- Debit_Card
    Controller o-- Airport 
    Plane o-- SeatClass
    Controller o-- FlightRoute
    Controller "1" --o "" Booking
    Booking --> Payment
    Booking <-- SeatClass
    Booking --> PassengerDetail
    Booking --> Promocode
    Account "1" <-- "" Booking
    Promocode -- Account
    Controller o-- Plane
    Plane --> SeatClass
    Account --> Userdetail
    Booking --> luggage
    Account --o Controller
    Payment -- Paymentmethod