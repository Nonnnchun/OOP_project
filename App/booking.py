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
        passenger_data = []
        person_count = int(form_data.get("person_count", "1"))
        
        for i in range(person_count):
            first_name = form_data.get(f"first_name_{i}", "")
            last_name = form_data.get(f"last_name_{i}", "")
            phone = form_data.get(f"phone_{i}", "")
            dob = form_data.get(f"dob_{i}", "")
            
            passenger = Passenger(
                firstname=first_name,
                lastname=last_name,
                phone=phone,
                dob=dob,
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
    
    passenger_items = []
    seat_prices = {"Economy": 500, "Business": 1200, "First Class": 2500}
    total_seat_price = 0
    
    seat_details = []
    for passenger in booking.passengers:
        seat_id = booking.passenger_seats.get(passenger.id, 'Not assigned')
        seat_class = "Economy"

        if seat_id != 'Not assigned':
            seat = next((s for s in flight.plane.seats if s.seat_id == seat_id), None)
            if seat and hasattr(seat, 'seat_type'):
                seat_class = seat.seat_type
        
        seat_price = seat_prices.get(seat_class, 500)
        total_seat_price += seat_price
        
        seat_details.append({
            "id": seat_id,
            "class": seat_class,
            "price": seat_price
        })
        
        passenger_items.append(
            Div(
                P(f"Name: {passenger.firstname} {passenger.lastname}"),
                P(f"Contact: {passenger.phone}"),
                P(f"Seat: {seat_id} ({seat_class}) - ${seat_price}"),
                cls="passenger-item"
            )
        )
    
    luggage_weight_price = form_data.get("luggage_weight_price", "").strip()

    total_price = total_seat_price + float(luggage_weight_price)
    
    booking.create_payment(total_price)

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
            Div(
                Div(
                    Div("Seat Prices:", cls="price-label"),
                    Div(f"${total_seat_price}", cls="price-value"),
                    cls="price-row"
                ),
                Div(
                    Div("Luggage Fee:", cls="price-label"),
                    Div(f"${luggage_weight_price}", cls="price-value"),
                    cls="price-row"
                ),
                Div(
                    Div("Total Price:", cls="price-label"),
                    Div(f"${total_price}", cls="price-value"),
                    cls="total-price price-row"
                ),
                cls="price-summary"
            ),
            cls="section"
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
    return (
        Title("Manage Bookings"), 
        Container(
            H1("Manage Bookings", style=f"color: {YELLOW_DARK}; text-align: center; margin-bottom: 30px;"),
            Button("Back to Home", 
                   hx_get="/home", 
                   hx_target="body", 
                   hx_swap="outerHTML",
                   style=f"background-color: {YELLOW_ACCENT}; color: {YELLOW_TEXT}; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px;"
            ),
            get_booking_table(),
            Div(id="edit-section"),
            Dialog(id="confirm-dialog")
        )
    )

@rt("/edit-booking/{ref}", methods=["GET", "POST"])
def edit_booking_page(ref: str, flight_date: str = "", passenger_seats: list = None, outbound_seat: str = "", confirm: bool = False):
    booking = Booking.get_booking_by_ref(ref)

    if not booking:
        return Div(H3(f"Booking with ref {ref} not found.", style=f"color: red;"))

    route = booking.flight
    
    # Get available seats
    available_seats = route.outbound_seats
    
    # Show available departure and arrival dates as pairs
    date_options = [
        Option(f"{departure} → {arrival}", value=f"{departure}|{arrival}") 
        for departure, arrival in zip(route.available_departure_dates, route.available_arrival_dates)
    ]

    # Get passengers
    passengers = booking.passengers if hasattr(booking, 'passengers') and booking.passengers else []
    
    # Get current passenger seat assignments (if available)
    current_seats = {}
    if hasattr(booking, 'passenger_seats') and booking.passenger_seats:
        current_seats = booking.passenger_seats
    elif len(passengers) == 1 and hasattr(booking, 'outbound_seat'):
        # For backward compatibility with single passenger bookings
        passenger = passengers[0]
        passenger_id = getattr(passenger, 'id', f"{passenger.firstname}_{passenger.lastname}")
        current_seats[passenger_id] = booking.outbound_seat.seat_id if hasattr(booking.outbound_seat, 'seat_id') else booking.outbound_seat

    if confirm:
        # Handle form submission for saving changes
        print(f"Processing form submission with passenger_seats: {passenger_seats}")
        
        # Process passenger seats if available
        selected_seats = {}
        if passenger_seats:
            # Handle each passenger seat selection
            for ps in passenger_seats:
                if ":" in ps:
                    # Format is "passenger_id:seat_id"
                    passenger_id, seat_id = ps.split(":", 1)
                    selected_seat = next((s for s in available_seats if s.seat_id == seat_id), None)
                    if selected_seat:
                        selected_seats[passenger_id] = selected_seat
                        print(f"Selected seat {seat_id} for passenger {passenger_id}")
        
        # Handle single outbound seat if no passenger seats were provided and outbound_seat is available
        elif outbound_seat and not passengers:
            selected_seat = next((s for s in available_seats if s.seat_id == outbound_seat), None)
            if selected_seat:
                booking.outbound_seat = selected_seat
        
        if flight_date:
            # Split flight_date into departure and arrival
            departure, arrival = flight_date.split("|")
            booking.flight_date = departure
            booking.arrival_time = arrival
            
            # Set passenger seats directly on the booking object if we have any
            if selected_seats:
                booking.passenger_seats = selected_seats
                print(f"Updated booking.passenger_seats to: {booking.passenger_seats}")

            # Save the changes
            if hasattr(booking, 'edit'):
                booking.edit(flight_date=departure, arrival_time=arrival)
            
            # Also manually preserve seats even if edit doesn't save them
            if hasattr(booking, 'save'):
                booking.save()
                
            # Debug info
            print(f"After edit: booking.passenger_seats = {booking.passenger_seats if hasattr(booking, 'passenger_seats') else 'N/A'}")
            
            # Refresh the page to show the updated booking information
            return get_booking_table(), Script("document.getElementById('manage-booking-table').outerHTML = ''; window.location.reload();")

    # Default value for flight date selection
    flight_date_value = ""
    if booking.flight_date and booking.arrival_time:
        flight_date_value = f"{booking.flight_date}|{booking.arrival_time}"

    # Create the form
    form_content = [
        # Flight Section
        H4(f"Flight: {route.origin} → {route.destination}", style=f"color: {YELLOW_DARK}; margin-top: 20px; border-bottom: 1px solid {YELLOW_BORDER};"),
        Label("Departure and Arrival Date"),
        Select(
            name="flight_date",
            *date_options,
            value=flight_date_value
        ),
    ]
    
    # Create seat selection for each passenger
    if passengers:
        form_content.append(H4("Select Seats for Passengers", style=f"color: {YELLOW_DARK}; margin-top: 20px; border-bottom: 1px solid {YELLOW_BORDER};"))
        
        # Create options for seat selection
        seat_options = [
            Option(f"{seat.seat_id} ({seat.seat_type})", value=seat.seat_id) for seat in available_seats
        ]
        
        for passenger in passengers:
            passenger_id = getattr(passenger, 'id', f"{passenger.firstname}_{passenger.lastname}")
            current_seat = ""
            
            # Try to get the current seat for this passenger
            if passenger_id in current_seats:
                seat = current_seats[passenger_id]
                current_seat = seat.seat_id if hasattr(seat, 'seat_id') else str(seat)
            
            # Create hidden field to pass passenger ID along with the seat
            passenger_id_field = Input(
                type="hidden",
                name=f"passenger_id_{passenger_id}",
                value=passenger_id
            )
            
            form_content.extend([
                Label(f"Seat for {passenger.firstname} {passenger.lastname}"),
                passenger_id_field,
                # Modify the select to make it work properly with form submission
                Select(
                    name=f"passenger_seats",  # Use consistent name for all passenger seat selects
                    *seat_options,
                    value=current_seat,  # Just use the seat ID as value
                    # Remove hx-post and hx-trigger that may be interfering
                )
            ])
    else:
        # Fallback for single seat selection if no passengers are defined
        current_seat = ""
        if hasattr(booking, 'outbound_seat'):
            current_seat = booking.outbound_seat.seat_id if hasattr(booking.outbound_seat, 'seat_id') else str(booking.outbound_seat)
        
        form_content.extend([
            Label("Select Seat"),
            Select(
                name="outbound_seat",
                *[Option(f"{seat.seat_id} ({seat.seat_type})", value=seat.seat_id) for seat in available_seats],
                value=current_seat
            )
        ])
    
    # Add the save button
    form_content.append(
        Button("Save Changes", type="submit",
            hx_post=f"/edit-booking/{ref}?confirm=true",
            hx_include="closest form",
            hx_target="#manage-booking-table",
            hx_swap="outerHTML",
            style=f"background-color: {YELLOW_PRIMARY}; padding: 15px 32px; font-size: 18px; color: {YELLOW_TEXT}; border-radius: 8px; border: none; transition: background-color 0.3s ease; cursor: pointer; width: 100%; margin-top: 20px;",
            onmouseover=f"this.style.backgroundColor='{YELLOW_DARK}';",  
            onmouseout=f"this.style.backgroundColor='{YELLOW_PRIMARY}';"
        )
    )

    return Card(
        H3(f"Edit Booking {ref}", style=f"color: {YELLOW_PRIMARY}; margin-bottom: 20px;"),
        Form(
            *form_content,
            method="post",
            style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;"
        ),
        style=f"border: 1px solid {YELLOW_BORDER}; border-radius: 8px; padding: 20px; "
    )

@rt("/cancel-booking/{ref}")
def cancel_booking(ref: str):
    booking = Booking.get_booking_by_ref(ref)  
    if booking:
        booking.cancel()  
        return get_booking_table(), Div(id="edit-section"), Script("window.location.reload();")
    return RedirectResponse("/manage-booking?error=Booking+not+found")

@rt("/confirm-cancel/{ref}")
def confirm_cancel(ref: str):
    return Dialog(
        P(f"Confirm Cancellation", style=f"font-size: 24px; color: {YELLOW_DARK}; font-weight: bold; margin-bottom: 15px;"),
        P(f"Are you sure you want to cancel booking {ref}?", style="font-size: 16px; margin-bottom: 20px;"),
        Div(
            Button("Yes, Cancel",
                   hx_post=f"/cancel-booking/{ref}",
                   hx_target="#manage-booking-table",
                   hx_swap="outerHTML",
                   cls="danger",
                   onclick="this.closest('dialog').close();",
                   style="padding: 10px 20px;"),  
            Button("Close", 
                   onclick="this.closest('dialog').close()", 
                   cls="secondary",
                   style="padding: 10px 20px;"),
            style="display: flex; justify-content: space-between; gap: 10px;"
        ),
        open=True,
        id="confirm-dialog",
        style=f"border: 2px solid {YELLOW_BORDER}; border-radius: 8px; padding: 20px;"
    )

def get_booking_table():
    if not Booking.bookings:
        return Div(
            H3("No bookings available", style=f"color: {YELLOW_DARK}; text-align: center; margin: 30px 0;")
        )
    
    # Create table headers
    table_headers = [
        Th("Ref"), 
        Th("Passengers"), 
        Th("Departure → Arrival"), 
        Th("Route"), 
        Th("Seats"),
        Th("Price"), 
        Th("Luggage"), 
        Th("Payment Method"), 
        Th("Status"),  
        Th("Actions")
    ]
    
    booking_rows = []
    for b in Booking.bookings:
        # Get the booking reference
        ref = b.booking_reference
        
        # Get passenger information directly from object
        passenger_info = ""
        if hasattr(b, 'passengers') and b.passengers:
            if len(b.passengers) == 1:
                passenger = b.passengers[0]
                passenger_info = f"{passenger.firstname} {passenger.lastname}"
            else:
                passenger_names = [f"{p.firstname} {p.lastname}" for p in b.passengers]
                passenger_info = ", ".join(passenger_names)
        
        # Ensure Departure → Arrival information is displayed
        dep_arrival_info = ""
        if hasattr(b, 'flight_date') and b.flight_date:
            # Also check for arrival_time
            if hasattr(b, 'arrival_time') and b.arrival_time:
                dep_arrival_info = f"{b.flight_date} → {b.arrival_time}"
            else:
                dep_arrival_info = f"{b.flight_date}"  # Show at least the flight date
        
        # Create row data for each booking
        row_data = [
            Td(ref),
            Td(passenger_info),
            Td(dep_arrival_info, style="font-weight: bold;"),  # Make it bold for visibility
        ]

        # Add route information
        route_info = "Route info unavailable"
        if hasattr(b, 'flight') and hasattr(b.flight, 'origin') and hasattr(b.flight, 'destination'):
            route_info = f"{b.flight.origin} → {b.flight.destination}"
        elif hasattr(b, 'route') and hasattr(b.route, 'origin') and hasattr(b.route, 'destination'):
            route_info = f"{b.route.origin} → {b.route.destination}"
        row_data.append(Td(route_info))
        
        # Get seats information
        seats_info = ""
        if hasattr(b, 'passenger_seats') and b.passenger_seats:
            # Show seats for each passenger
            seats = []
            for passenger_id, seat in b.passenger_seats.items():
                # Try to find passenger name from passenger_id
                passenger_name = passenger_id
                if hasattr(b, 'passengers') and b.passengers:
                    for p in b.passengers:
                        p_id = getattr(p, 'id', f"{p.firstname}_{p.lastname}")
                        if p_id == passenger_id:
                            passenger_name = f"{p.firstname} {p.lastname}"
                            break
                
                seat_id = seat.seat_id if hasattr(seat, 'seat_id') else str(seat)
                seats.append(f"{passenger_name}: {seat_id}")
            
            seats_info = ", ".join(seats)
        elif hasattr(b, 'outbound_seat'):
            # Fallback for single seat
            seats_info = b.outbound_seat.seat_id if hasattr(b.outbound_seat, 'seat_id') else str(b.outbound_seat)
        elif hasattr(b, 'seat'):
            # Alternative attribute name
            seats_info = b.seat.seat_id if hasattr(b.seat, 'seat_id') else str(b.seat)
        
        row_data.append(Td(seats_info))
        
        # Add price and other details
        price_info = ""
        if hasattr(b, 'payment') and hasattr(b.payment, 'price'):
            price_info = f"{b.payment.price} THB"
        elif hasattr(b, 'price'):
            price_info = f"{b.price} THB"
        
        luggage_info = ""
        if hasattr(b, 'luggage_weight'):
            luggage_info = f"{b.luggage_weight} kg"
        elif hasattr(b, 'luggage'):
            luggage_info = f"{b.luggage} kg"
        
        payment_method_info = ""
        if hasattr(b, 'payment') and hasattr(b.payment, 'method'):
            if hasattr(b.payment.method, 'method_id'):
                payment_method_info = b.payment.method.method_id
        elif hasattr(b, 'payment_method'):
            payment_method_info = b.payment_method
            
        row_data.extend([
            Td(price_info),
            Td(luggage_info),
            Td(payment_method_info),
            Td(b.status if hasattr(b, 'status') else "", 
               style="font-weight: bold; color: " + 
               ("#4CAF50" if hasattr(b, 'status') and b.status == "Confirmed" else 
                "#F44336" if hasattr(b, 'status') and b.status == "Cancelled" else 
                YELLOW_DARK)),
            Td(
                Button("Edit", 
                       hx_get=f"/edit-booking/{ref}", 
                       hx_target="#edit-section", 
                       hx_swap="outerHTML",
                       style=f"background-color: {YELLOW_PRIMARY}; color: {YELLOW_TEXT};"
                      ) if hasattr(b, 'status') and b.status != "Cancelled" else "",
                Button("Cancel", 
                       cls="danger", 
                       hx_get=f"/confirm-cancel/{ref}", 
                       hx_target="#confirm-dialog", 
                       hx_swap="outerHTML"
                      ) if hasattr(b, 'status') and b.status != "Cancelled" else ""
            ) 
        ])
        print(f"Booking {ref}: Departure = {b.flight_date}, Arrival = {b.arrival_time}")
        booking_rows.append(Tr(*row_data))

    return Div(
        Table(
            Thead(Tr(*table_headers)),
            Tbody(*booking_rows),
            id="manage-booking-table",
            style=f"border: 1px solid {YELLOW_BORDER}; border-radius: 4px; overflow: hidden;"
        ),
        style="overflow-x: auto;"
    )