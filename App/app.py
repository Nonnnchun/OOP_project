from fasthtml.common import *
from welcome import welcome_app
from register_login import register_login_app
from home import home_app
from flightsearch import flightsearch_app
from seat import seat_app
from luggage import luggage_app
from passenger import passenger_app
from booking import booking_app
from payment import payment_app
from promocode import promocode_app

app, rt = fast_app(routes=[
    Route('/', welcome_app, name='welcome'),
    Route('/register', register_login_app, name='register'),
    Route('/check-password', register_login_app, name='checkpassword'),
    Route('/check-confirm-password', register_login_app, name='checkconfirmpassword'),
    Route('/check-confirm-password', home_app, name='checkconfirmpassword'),
    Route('/login', register_login_app, name='login'),
    Route('/check-password', home_app, name='checkpassword'),
    Route('/home', home_app, name='home'),
    Route('/logout', home_app, name='logout'),
    Route('/profile', home_app, name='profile'),
    Route('/password', home_app, name='password'),
    Route('/edit-profile', home_app, name='editprofile'),
    Route('/passwordCheck', home_app, name='changepassword'),
    Route('/flight_search', flightsearch_app, name='flightsearch'),
    Route('/search_results', flightsearch_app, name='result'),
    Route('/seat_map', seat_app, name='seatmap'),
    Route('/confirm_seat', seat_app, name='confirmseat'),
    Route('/luggage_calculator', luggage_app, name='luggage'),
    Route('/luggage_results', luggage_app, name='luggageresults'),
    Route('/passenger_details', passenger_app, name='passenger'),
    Route('/booking_summary', booking_app, name='booking'),
    Route('/payment', payment_app, name='payment'),
    Route('/payment_confirmation', payment_app, name='paymentconfirmation'),
    Route('/manage-booking', booking_app, name='booking'),
    Route('/edit-booking/{ref}', booking_app, name='editbooking'),
    Route('/cancel-booking/{ref}', booking_app, name='cancelbooking'),
    Route('/confirm-cancel/{ref}', booking_app, name='confirmcancel'),
    Route('/promocode', promocode_app, name='promocode'),
    Route('/confirm-redeem/{code}', promocode_app, name='confirmpromo'),
    Route('/redeem/{code}', promocode_app, name='redeem'),
    
    ])

serve()