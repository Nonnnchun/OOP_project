from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
booking_app = app 

YELLOW_PRIMARY = "#FFD700"  # Golden yellow
YELLOW_SECONDARY = "#FFEE63"  # Light yellow
YELLOW_ACCENT = "#FFC107"  # Amber yellow
YELLOW_DARK = "#F9A825"  # Dark yellow
YELLOW_TEXT = "#333333"  # Dark text for contrast
YELLOW_BACKGROUND = "#FFFEF0"  # Very light yellow background
YELLOW_BORDER = "#FFB300"  # Border color


@rt("/booking_summary", methods=["POST"])
async def booking_summary(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()

    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")

    flight = controller.get_flight_by_id(booking.flight.flight_id)
    if not flight:
        return Title("Error"), H1("Flight not found")

    if not hasattr(booking, 'passengers') or not booking.passengers:
        person_count = int(form_data.get("person_count", "1"))
        passenger_data = []

        for i in range(person_count):
            passenger = Passenger(
                firstname=form_data.get(f"first_name_{i}", ""),
                lastname=form_data.get(f"last_name_{i}", ""),
                phone=form_data.get(f"phone_{i}", ""),
                dob=form_data.get(f"dob_{i}", "")
            )           
            passenger_data.append(passenger)

        booking.passengers = passenger_data

        seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
        if not isinstance(seat_ids, list):
            seat_ids = [seat_ids]

        booking.passenger_seats = {}
        for i, passenger in enumerate(booking.passengers):
            if i < len(seat_ids):
                booking.passenger_seats[passenger.id] = seat_ids[i]
                booking.add_seat(seat_ids[i])

    total_seat_price = 0
    passenger_items = []

    for passenger in booking.passengers:
        seat_id = booking.passenger_seats.get(passenger.id, 'Not assigned')
        seat_class = "Economy"
        seat_price = 0

        if seat_id != 'Not assigned':
            seat = next((s for s in flight.outbound_seats if s.seat_id == seat_id), None)
            if not seat:
                seat = next((s for s in flight.plane.seats if s.seat_id == seat_id), None)
            if seat:
                seat_class = seat.seat_type
                seat_price = seat.price

        total_seat_price += seat_price

        passenger_items.append(
            Div(
                P(f"Name: {passenger.firstname} {passenger.lastname}"),
                P(f"Contact: {passenger.phone}"),
                P(f"Seat: {seat_id} ({seat_class}) - ${seat_price}"),
                cls="passenger-item"
            )
        )

    luggage_weight_price = float(form_data.get("luggage_weight_price", "0"))
    total_price = total_seat_price + luggage_weight_price

    # Create or update payment
    if not booking.payment:
        booking.create_payment(total_price)
    else:
        booking.payment.price = total_price

    # Initialize prices
    original_price = booking.payment.price
    discounted_price = original_price

    # Handle Promo Code
    code = form_data.get("code", "").strip().upper()
    # Clean the code - remove any special characters and extra spaces
    code = ''.join(c for c in code if c.isalnum() or c.isdigit())
    print(f"🔍 Checking Promo Code: '{code}'")

    user = controller.get_logged_in_user()
    if user and code:
        discount_percent = user.userdetail.search_promo(code)
        
        if discount_percent > 0:
            booking.payment.discount_payment(discount_percent)
            discounted_price = booking.payment.price
            
            # Only mark promo as used if it's valid and applied successfully
            if user.userdetail.use_promo(code):
                print(f"✅ Promo applied: {discount_percent}% off | {original_price} -> {discounted_price}")
            else:
                print("⚠️ Failed to mark promo code as used")
        else:
            print("⚠️ Invalid or expired promo code")
    else:
        if not user:
            print("❌ No user logged in")
        if not code:
            print("ℹ️ No promo code provided")

    return Title("Booking Summary"), Div(
        Div(
            H1("Booking Summary"),
            P("Please review your booking details before confirming"),
            cls="header",
        ),

        Div(f"Booking Reference: {booking_ref}", cls="booking-ref"),

        Div(
            H2("Flight Details"),
            Div(
                P(f"Flight: {flight.origin} to {flight.destination}"),
                P(f"Departure: {flight.departure_time}"),
                P(f"Arrival: {flight.arrive_time}"),
                P(f"Aircraft: {flight.plane.aircraft}"),
                cls="flight-details",
            ),
            cls="section"
        ),

        Div(
            H2("Passengers"),
            Div(*passenger_items, cls="passenger-list"),
            cls="section",
        ),

        Div(
            H2("Luggage Information"),
            Div(
                P(f"Total Luggage Weight: {booking.luggage.kilogram} kg"),
                P(f"Luggage Fee: ${luggage_weight_price}"),
                cls="luggage-details",
            ),
            cls="section"
        ),

        Div(
            H2("Price Summary"),
            P(f"Seat Prices: ${total_seat_price}"),
            P(f"Luggage Fee: ${luggage_weight_price}"),
            P(f"Total Price: ${original_price}"),
            P(f"Price After Use Promocode: ${discounted_price}"),  
            cls="price-summary"
        ),

        Div(
            H2("Promocode"),
            Form(
                Div(
                    Label("Have a promocode?", for_="promocode-input"),
                    Input(id="code", type="text", name="code", placeholder="Enter promocode"),
                    Button("Apply", type="submit", cls="apply-btn"),
                    cls="promocode-form"
                ),
                Input(type="hidden", name="booking_ref", value=booking_ref),
                Input(type="hidden", name="luggage_weight_price", value=str(luggage_weight_price)),
                *[Input(type="hidden", name=k, value=v) for k, v in form_data.items() if k != "code" and k != "booking_ref" and k != "luggage_weight_price"],
                action="/booking_summary",
                method="post"
            ),
            cls="section promocode-section"
        ),

        Div(
            Form(
                Button("Back", type="button", cls="back-btn", onclick="history.back()"),
                Input(type="hidden", name="booking_ref", value=booking_ref),
                Input(type="hidden", name="total_price", value=str(total_price)),
                Button("Confirm and Pay", type="submit", cls="confirm-btn"),
                action="/payment",
                method="post"
            ),
            cls="action-buttons"
        ),
        cls="container"
    )
    
@rt("/manage-booking")
def manage_booking():
    """Main page showing all bookings with edit and cancel options"""
    return Title("Manage Bookings"), Container(
        Div(
            A("← Back to Home", 
              href="/home",
              style="display: inline-block; margin: 20px; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px; transition: background-color 0.3s;"),
            style="text-align: left;"
        ),
        H1("Manage Your Bookings", style="color: #ffee63; text-align: center; margin-bottom: 30px;"),
        P("View, edit or cancel your flight bookings below.", style="text-align: center; margin-bottom: 20px;"),
        get_booking_table(),
        Div(id="edit-section"),
        Dialog(id="confirm-dialog")
    )

@rt("/edit-booking/{ref}", methods=["GET", "POST"])
async def edit_booking_page(ref: str, flight_date: str = "", confirm: bool = False, request: Request = None):
    """Edit a specific booking"""
    booking = next((b for b in Booking.bookings if b.booking_reference == ref), None)
    if not booking:
        return Div(H3(f"Booking not found.", style="color: red; text-align: center;"))

    if confirm and request:
        form_data = await request.form()
        # Process the changes
        if flight_date and "|" in flight_date:
            departure, arrival = flight_date.split("|")
            booking.flight_date = departure
            booking.arrival_time = arrival

        # Handle multiple seat selections from form data
        for key, value in form_data.items():
            if key.startswith("passenger_seat_"):
                passenger_id = key.replace("passenger_seat_", "")
                new_seat_id = value
                
                # Free up old seat if exists
                old_seat_id = booking.passenger_seats.get(passenger_id)
                if old_seat_id:
                    old_seat = next((s for s in booking.flight.plane.seats if s.seat_id == old_seat_id), None)
                    if old_seat:
                        old_seat.update_seat_status(True)
                
                # Assign new seat
                new_seat = next((s for s in booking.flight.plane.seats if s.seat_id == new_seat_id), None)
                if new_seat:
                    new_seat.update_seat_status(False)
                    booking.passenger_seats[passenger_id] = new_seat_id

        return get_booking_table(), Script("window.location.reload();")

    # Create the edit form
    date_options = [
        Option(f"{departure} → {arrival}", value=f"{departure}|{arrival}") 
        for departure, arrival in zip(booking.flight.available_departure_dates, booking.flight.available_arrival_dates)
    ]

    # Create seat selection for each passenger
    passenger_seat_forms = []
    if hasattr(booking, 'passengers') and hasattr(booking, 'passenger_seats'):
        for passenger in booking.passengers:
            current_seat_id = booking.passenger_seats.get(passenger.id, "")
            
            # Get the current seat to determine its class
            current_seat = next((seat for seat in booking.flight.plane.seats 
                               if seat.seat_id == current_seat_id), None)
            
            if current_seat:
                # Only show seats of the same class as the current seat
                seat_type = current_seat.seat_type
                
                # Get available seats of the same class plus current seat
                available_seats = [seat for seat in booking.flight.plane.seats 
                                 if (seat.is_available() or seat.seat_id == current_seat_id)
                                 and seat.seat_type == seat_type]
                
                seat_options = [
                    Option(
                        f"{seat.seat_id} ({seat.seat_type})", 
                        value=seat.seat_id,
                        selected=(seat.seat_id == current_seat_id)
                    ) for seat in available_seats
                ]
                
                passenger_seat_forms.append(
                    Div(
                        H4(f"Seat for {passenger.firstname} {passenger.lastname}", 
                           style="color: #ffee63; margin-bottom: 10px;"),
                        P(f"Current seat class: {seat_type}", 
                          style="color: #fff; margin-bottom: 10px;"),
                        Select(
                            name=f"passenger_seat_{passenger.id}",
                            *seat_options,
                            style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;"
                        ),
                        style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px;"
                    )
                )

    return Card(
        H3(f"Edit Booking {ref}", style="color: #ffee63; text-align: center; margin-bottom: 20px;"),
        Form(
            Div(
                H4("Flight Date", style="color: #ffee63; margin-bottom: 10px;"),
                Select(
                    name="flight_date",
                    *date_options,
                    value=f"{booking.flight_date}|{booking.arrival_time}",
                    style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ddd;"
                ),
                style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px;"
            ),
            *passenger_seat_forms,
            Button("Save Changes", 
                type="submit",
                hx_post=f"/edit-booking/{ref}?confirm=true",
                hx_target="#manage-booking-table",
                hx_swap="outerHTML",
                style="""
                    background-color: #4CAF50; 
                    color: white; 
                    padding: 12px 24px; 
                    border: none; 
                    border-radius: 4px; 
                    cursor: pointer;
                    font-weight: bold;
                    width: 100%;
                    transition: background-color 0.3s;
                """
            ),
            method="post",
            style="display: flex; flex-direction: column; gap: 10px; padding: 20px;"
        ),
        style="max-width: 500px; margin: 0 auto; background-color: #333; padding: 20px; border-radius: 10px;"
    )

def get_booking_table():
    """Generate the bookings table, but only for the logged-in user."""
    if not controller.logged_in_user:
        return Div(
            H3("You must be logged in to view bookings.", style="color: red; text-align: center;")
        )

    # 🔥 Filter bookings to only show those belonging to the logged-in user
    user_bookings = [b for b in Booking.bookings if b.user_email == controller.logged_in_user.email]

    if not user_bookings:
        return Div(
            H3("No bookings available", style="color: #ff6347; text-align: center;")
        )

    booking_rows = []
    for booking in user_bookings:  # ✅ Only show the current user's bookings
        seat_info = []
        if hasattr(booking, 'passenger_seats'):
            for passenger_id, seat_id in booking.passenger_seats.items():
                passenger = next((p for p in booking.passengers if p.id == passenger_id), None)
                if passenger:
                    seat_info.append(Div(f"{passenger.firstname}: {seat_id}"))
        seat_info_container = Div(*seat_info) if seat_info else "Not assigned"

        flight_info = f"{booking.flight.origin} → {booking.flight.destination}"

        passenger_info = []
        if hasattr(booking, 'passengers'):
            for passenger in booking.passengers:
                passenger_info.append(Div(f"{passenger.firstname} {passenger.lastname}"))
        passenger_info_container = Div(*passenger_info) if passenger_info else "No passengers"

        total_price = 0
        if hasattr(booking, 'passenger_seats'):
            for seat_id in booking.passenger_seats.values():
                seat = next((s for s in booking.flight.plane.seats if s.seat_id == seat_id), None)
                if seat:
                    total_price += seat.price

        if hasattr(booking, 'luggage_weight') and booking.luggage_weight > 0:
            luggage = Luggage(booking.luggage_weight)
            total_price += luggage.calculate_price()

        luggage_info = f"{booking.luggage_weight} kg" if hasattr(booking, 'luggage_weight') and booking.luggage_weight > 0 else "No luggage"

        payment_info = "Not paid"
        if booking.payment and booking.payment.method:
            payment_info = f"{booking.payment.method.method_id} ({booking.payment.method.card_number[-4:]})"

        action_buttons = []
        if booking.status != "Cancelled":
            action_buttons.extend([
                Button("Edit", 
                       hx_get=f"/edit-booking/{booking.booking_reference}", 
                       hx_target="#edit-section", 
                       hx_swap="outerHTML",
                       style="background-color: #4CAF50; color: white; margin-right: 5px; border: none; padding: 5px 10px; border-radius: 4px;"),
                Button("Cancel", 
                       cls="danger", 
                       hx_get=f"/confirm-cancel/{booking.booking_reference}", 
                       hx_target="#confirm-dialog", 
                       hx_swap="outerHTML",
                       style="background-color: #ff6347; color: white; border: none; padding: 5px 10px; border-radius: 4px;")
            ])

        booking_rows.append(
            Tr(
                Td(booking.booking_reference),
                Td(passenger_info_container, style="padding: 10px;"),
                Td(f"{booking.flight_date} → {booking.arrival_time}"),
                Td(flight_info),
                Td(seat_info_container, style="padding: 10px;"),
                Td(f"{total_price:,} THB"),
                Td(luggage_info),
                Td(payment_info),
                Td(booking.status),
                Td(*action_buttons)
            )
        )

    return Table(
        Thead(Tr(
            Th("Reference"),
            Th("Passengers"),
            Th("Flight Date"),
            Th("Route"),
            Th("Seats"),
            Th("Price"),
            Th("Luggage"),
            Th("Payment"),
            Th("Status"),
            Th("Actions")
        )),
        Tbody(*booking_rows),
        id="manage-booking-table",
        style="""
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            overflow: hidden;
        """
    )

@rt("/cancel-booking/{ref}")
def cancel_booking(ref: str):
    """Cancel a booking"""
    booking = next((b for b in Booking.bookings if b.booking_reference == ref), None)
    if booking:
        # Explicitly release all seats before cancelling
        if hasattr(booking, 'passenger_seats') and booking.passenger_seats:
            for passenger_id, seat_id in booking.passenger_seats.items():
                # Find the seat in the flight's plane seats
                seat = next((s for s in booking.flight.plane.seats if s.seat_id == seat_id), None)
                if seat:
                    # Mark the seat as available
                    seat.update_seat_status(True)
                    print(f"Released seat {seat_id} for booking {ref}")
        
        # Now cancel the booking
        booking.cancel()
        return get_booking_table(), Script("window.location.reload();")
    return RedirectResponse("/manage-booking?error=Booking+not+found")

@rt("/confirm-cancel/{ref}")
def confirm_cancel(ref: str):
    """Show cancellation confirmation dialog"""
    return Dialog(
        H3("Confirm Cancellation", style="color: #ff6347; margin-bottom: 20px;"),
        P(f"Are you sure you want to cancel booking {ref}?"),
        Div(
            Button("Yes, Cancel",
                   hx_post=f"/cancel-booking/{ref}",
                   hx_target="#manage-booking-table",
                   hx_swap="outerHTML",
                   cls="danger",
                   onclick="this.closest('dialog').close();",
                   style="background-color: #ff6347; color: white; margin-right: 10px;"),  
            Button("No, Keep Booking", 
                   onclick="this.closest('dialog').close()", 
                   cls="secondary",
                   style="background-color: #4CAF50; color: white;")
        ),
        open=True,
        id="confirm-dialog",
        style="padding: 20px; border-radius: 8px;"
    )
