```mermaid

classDiagram
    direction TB
    
    %% Controller Class
    class Controller {
        -planes[]
        -accounts[]
        -logged_in_user
        -flights[]
        -bookings[]
        -next_flight_id
        -luggage_system
        -airports[]
        +register(email, password, firstname, lastname)
        +login(email, password)
        +logout()
        +get_logged_in_user()
        +get_flight_by_id(flight_id)
        +create_booking(flight_id, luggage_kg)
        +add_booking_history(booking)
        +search_flights(origin, destination, date)
        +add_flight(flight)
        +get_flight(flight_id)
        +update_flight(updated_flight)
        +delete_flight(flight_id)
        +filter_flights(query, available_only)
        +add_plane(plane)
        +add_airport(airport)
        +generate_flight_id()
        +calculate_luggage_price(luggage_kg)
        +get_booking(booking_reference)
    }

    %% Seat Class
    class Seat {
        -seat_id
        -seat_type
        -price
        -available
        +update_seat_status(available)
        +is_available()
    }

    %% Airport Class
    class Airport {
        -name
        -code
        +__str__()
    }
    
    %% Plane Class
    class Plane {
        -plane_id
        -aircraft
        -seats[]
        +_generate_seats()
        +get_available_seats(seat_type)
    }

    %% Booking Class
    class Booking {
        -booking_reference
        -flight
        -outbound_seat
        -return_seat
        -passengers[]
        -passenger_seats[]
        -luggage_weight
        -luggage
        -payment
        -status
        -flight_date
        -arrival_time
        -return_flight_date
        -return_arrival_time
        +add_luggage(kilogram)
        +add_passenger(passenger)
        +add_seat(seat_id)
        +add_return_seat(seat_id)
        +create_payment(price)
        +update_booking_status(status)
        +set_flight_dates(flight_date, arrival_time)
        +set_return_flight_dates(return_flight_date, return_arrival_time)
        +edit(flight_date, arrival_time, outbound_seat, return_flight_date, return_arrival_time, return_seat)
        +cancel()
        +calculate_refund()
        +process_refund()
        +get_booking_by_ref(ref)
    }

    %% Luggage Class
    class Luggage {
        -kilogram
        -price
        +calculate_price()
    }

    %% LuggagePricingSystem Class
    class LuggagePricingSystem {
        +calculate_luggage_price(luggage)
    }

    %% Payment Class
    class Payment {
        -price
        -method
        -status
        +process_payment(method, card_number, cvv, exp)
        +refund(amount)
        +discount_payment(discount_percent)
    }

    %% Account Class
    class Account {
        -email
        -password
        -userdetail
        -booking_history[]
        +check_password(password)
        +change_password(old_password, new_password, confirm_new_password)
    }
    
    %% UserDetail Class
    class UserDetail {
        -firstname
        -lastname
        -points
        -birthday
        -gender
        -identification
        -nationality
        -phone_number
        -address
        -promocode_list
        -booking_list
        -redeemed_codes
        +edit_profile(firstname, lastname, phone_number, address, birthday, gender, nationality)
        +redeem_promocode(promo)
        +get_owned_codes(promotion_codes)
        +search_promo(code)
        +use_promo(code)
    }
    
    %% PaymentMethod Class (Abstract)
    class PaymentMethod {
        <<Abstract>>
        -method_id
        +process_payment()*
    }

    %% ATMCard Class
    class ATMCard {
        -card_number
        -card_CVV
        -card_EXP
        +validate_card()
    }

    %% CreditCard Class
    class CreditCard {
        +process_payment()
    }

    %% DebitCard Class
    class DebitCard {
        -fee: 7%
        +calculate_fee()
        +process_payment()
    }

    %% Promocode Class
    class Promocode {
        -code
        -points
        -discount_percent
        -expiration_date
        -description
        +can_redeem(user_points)
        +is_expired()
    }

    %% FlightRoute Class
    class FlightRoute {
        -flight_id
        -origin_airport
        -destination_airport
        -departure_time
        -arrive_time
        -plane
        -available_departure_dates
        -available_arrival_dates
        -return_departure_dates
        -return_arrival_dates
        -outbound_seats
        -return_seats
        +display_flight_info()
        +is_round_trip()
        +get_routes()
        +add_outbound_seats(seats)
        +add_return_seats(seats)
    }

    %% Passenger Class
    class Passenger {
        -firstname
        -lastname
        -phone
        -dob
    }

    %% Relationships
    Controller "1" *-- "*" Airport: manages
    Controller "1" *-- "*" Plane: manages
    Controller "1" *-- "*" FlightRoute: manages
    Controller "1" *-- "*" Booking: manages
    Controller "1" *-- "1" LuggagePricingSystem: uses
    Controller "1" *-- "*" Account: manages
    
    Plane "1" *-- "*" Seat: contains
    
    Booking "1" --> "1" FlightRoute: references
    Booking "1" --> "0..1" Seat: outbound_seat
    Booking "1" --> "0..1" Seat: return_seat
    Booking "1" --> "*" Passenger: has
    Booking "1" --> "0..1" Luggage: has
    Booking "1" --> "0..1" Payment: has
    
    Account "1" --> "1" UserDetail: has
    Account "1" --> "*" Booking: booking_history
    
    UserDetail "1" --> "*" Promocode: redeemed_codes
    
    Payment "1" --> "0..1" PaymentMethod: uses
    
    PaymentMethod <|-- ATMCard: extends
    ATMCard <|-- CreditCard: extends
    ATMCard <|-- DebitCard: extends
    
    LuggagePricingSystem "1" --> "*" Luggage: calculates price
