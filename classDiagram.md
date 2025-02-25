```mermaid

classDiagram
    direction TB
    class Controller {
        -plane_list
        -account_list
        -flightRoute_list
        +flight_search()
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
        -seat

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
        -PurchasedHistory
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
        -passengerType
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
    Plane o-- Seat
    Controller o-- FlightRoute
    Controller "1" --o "" Booking
    Booking --> Payment
    Booking <-- Seat
    Booking --> PassengerDetail
    Booking --> Promocode
    Account "1" <-- "" Booking
    Promocode -- Account
    Controller o-- Plane
    Plane --> Seat
    Account --> Userdetail
    Booking --> luggage
    Account --o Controller
    Payment -- Paymentmethod