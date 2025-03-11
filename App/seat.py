from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
seat_app = app 

@rt("/seat_map", methods=["GET", "POST"])
async def seat_map(request):

    max_seat_count = 5

    form_data = await request.form() if request.method == "POST" else request.query_params

    flight_id = form_data.get("flight_id", "").strip()
    flight = controller.get_flight_by_id(flight_id)

    if not flight:
        return Title("Error"), H1("Flight not found")

    styles = Style("""
        body { font-family: Arial, sans-serif; background-color: #000000; color: #333; }
        .container { background: white; padding: 20px; border-radius: 10px; 
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); max-width: 800px; margin: 0 auto; }
        .seat-map { display: flex; flex-direction: column; gap: 5px; margin: 20px 0; }
        .row { display: flex; justify-content: center; gap: 5px; margin-bottom: 5px; }
        .seat { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;
                border-radius: 5px; font-size: 12px; position: relative; }
        .seat-checkbox { position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
        .seat-checkbox:checked + .seat-label { border: 2px solid #FF0000; }
        .seat-label { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
        
        /* Seat classes */
        .economy { background-color: #A0D6B4; } /* Light green for economy */
        .business { background-color: #8BB5FE; } /* Light blue for business */
        .first-class { background-color: #F3B5C1; } /* Light pink for first class */
        
        /* Seat availability */
        .available { border: 1px solid #888; cursor: pointer; }
        .booked { background-color: #ddd; color: #999; cursor: not-allowed; }
        
        /* Legend */
        .legend { display: flex; justify-content: center; gap: 15px; margin-bottom: 20px; }
        .legend-item { display: flex; align-items: center; gap: 5px; font-size: 12px; }
        .legend-color { width: 15px; height: 15px; border-radius: 3px; }
        
        /* Submit button */
        .submit-btn { background-color: #FFEB99; padding: 10px; font-size: 16px;
                     border: 2px solid #F9D01C; border-radius: 8px; font-weight: bold;
                     cursor: pointer; transition: 0.3s ease; margin-top: 20px; width: 100%; }
        .submit-btn:hover { background-color: #F9D01C; }
        
        /* Disabled button style */
        .submit-btn.disabled {
            background-color: #f0f0f0;
            border-color: #ccc;
            color: #999;
            cursor: not-allowed;
        }
        
        /* Counter for selected seats */
        .seat-counter { font-weight: bold; margin: 10px 0; }
        
        /* Error message */
        .error-message { color: #e74c3c; font-weight: bold; margin: 10px 0; }
    """)

    # ✅ Ensure a booking is created
    if request.method == "GET":
        booking = controller.create_booking(flight_id)
        if not booking:
            return Title("Error"), H1("Could not create booking")
    else:
        booking_ref = form_data.get("booking_ref", "").strip()
        booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
        if not booking:
            return Title("Error"), H1("Booking not found")

    # Check for error message
    error = form_data.get("error", "")
    error_message = Div("Please select at least one seat to continue.", cls="error-message") if error == "no_seats" else ""

    # ✅ Seat Map Logic
    seat_rows = {}
    for seat in flight.plane.seats:
        row_num = ''.join(filter(str.isdigit, seat.seat_id))
        if row_num not in seat_rows:
            seat_rows[row_num] = []
        seat_rows[row_num].append(seat)

    seat_map_html = []
    for row_num in sorted(seat_rows.keys(), key=int):
        seats_in_row = sorted(seat_rows[row_num], key=lambda s: ''.join(filter(str.isalpha, s.seat_id)))
        seat_buttons = []

        for seat in seats_in_row:
            seat_class = "available" if seat.is_available() else "booked"
            seat_type_class = "economy" if seat.seat_type == "Economy" else "business" if seat.seat_type == "Business" else "first-class"

            if seat.is_available():
                seat_buttons.append(
                    Div(
                        Input(type="checkbox", name="seat_ids", value=seat.seat_id, 
                              cls="seat-checkbox", 
                              onclick="checkSeatLimit(this)"),
                        Div(seat.seat_id, cls="seat-label"),
                        cls=f"seat {seat_class} {seat_type_class}"
                    )
                )
            else:
                seat_buttons.append(Div(seat.seat_id, cls=f"seat {seat_class} {seat_type_class}"))

        seat_map_html.append(Div(*seat_buttons, cls="row"))

    legend = Div(
        Div(Div(cls="legend-color economy"), "Economy", cls="legend-item"),
        Div(Div(cls="legend-color business"), "Business", cls="legend-item"),
        Div(Div(cls="legend-color first-class"), "First Class", cls="legend-item"),
        Div(Div(cls="legend-color available"), "Available", cls="legend-item"),
        Div(Div(cls="legend-color booked"), "Booked", cls="legend-item"),
        cls="legend"
    )

    # Javascript to limit seat selection to 5 and enforce at least 1 seat selection
    seat_limit_script = Script("""
        function checkSeatLimit(checkbox) {
            var checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
            var maxSeats = 5; // Max seat count
            var submitButton = document.getElementById('submit_button');
            
            document.getElementById('selected_seat_count').value = checkboxes.length;
            document.getElementById('selected-count').textContent = checkboxes.length;
            
            // Disable or enable submit button based on selection count
            if (checkboxes.length === 0) {
                submitButton.disabled = true;
                submitButton.classList.add('disabled');
            } else {
                submitButton.disabled = false;
                submitButton.classList.remove('disabled');
            }
            
            if (checkboxes.length > maxSeats) {
                checkbox.checked = false;
                alert(`You can only select up to ${maxSeats} seats`);
                
                // Update count after rejecting the check
                checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
                document.getElementById('selected_seat_count').value = checkboxes.length;
                document.getElementById('selected-count').textContent = checkboxes.length;
            }
        }
        
        // Initialize button state when page loads
        window.onload = function() {
            checkSeatLimit(null);
        }
        
        // Add form validation
        function validateForm(form) {
            var checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
            if (checkboxes.length === 0) {
                alert('Please select at least one seat to continue.');
                return false;
            }
            return true;
        }
    """)

    return Title("Seat Selection"), styles, seat_limit_script, Div(
        H1(f"Select Seats for Flight {flight_id}"),
        P(f"From {flight.origin} to {flight.destination}"),
        P(f"Departure: {flight.departure_time}"),
        Div("Selected seats: ", Span("0", id="selected-count"), Span(f"/{max_seat_count}", id="max-seat-count"), cls="seat-counter"),
        error_message,
        legend,
        Form(
            Div(*seat_map_html, cls="seat-map"),
            Input(type="hidden", name="booking_ref", value=booking.booking_reference),
            Input(type="hidden", name="flight_id", value=flight_id),
            Input(type="hidden", name="selected_seat_count", id="selected_seat_count", value="0"),
            Button("Continue with Selected Seats", type="submit", id="submit_button", cls="submit-btn"),
            action="/luggage_calculator",
            method="post",
            onsubmit="return validateForm(this);",
            cls="container"
        )
    )


@rt("/confirm_seat", methods=["POST"])
async def confirm_seat(request):
    try:
        form_data = await request.form()
        booking_ref = form_data.get("booking_ref", "")
        seat_id = form_data.get("seat_id", "")

        # Get the booking
        booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
        if not booking:
            return Title("Error"), H1("Booking not found")

        # Get the flight
        flight = controller.get_flight_by_id(booking.flight.flight_id)
        if not flight:
            return Title("Error"), H1("Flight not found")

        # Find the seat
        seat = next((s for s in flight.plane.seats if s.seat_id == seat_id), None)
        if not seat:
            return Title("Error"), H1("Seat not found")

        # 🚨 Double-check if the seat is already booked
        if not seat.is_available():
            return Title("Error"), H1(f"Seat {seat_id} is already booked! Please choose another seat.")

        # ✅ Proceed with booking
        if not booking.add_seat(seat_id):
            return Title("Error"), H1(f"Seat {seat_id} is already booked!")

        return RedirectResponse(f"/passenger_details?booking_ref={booking_ref}", status_code=303)

    except Exception as e:
        print(f"❌ Error processing seat confirmation: {e}")
        return Title("Error"), H1("An error occurred"), P(str(e))