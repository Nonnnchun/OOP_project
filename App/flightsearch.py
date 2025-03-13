from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
flightsearch_app = app 

@rt("/flight_search")
def search():
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #000000;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .form-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 320px;
            text-align: center;
        }
        .form-container select, .form-container input {
            width: 100%;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
            font-color:black
            background-color: #ffe600;
            cursor: pointer;
        }
        .search-btn {
            background-color: #FFEB99;
            padding: 10px;
            font-size: 16px;
            width: 100%;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
        }
        .search-btn:hover {
            background-color: #F9D01C;
        }
        .error-message {
            color: red;
            font-size: 14px;
            margin-top: 5px;
            display: none;
        }
    """)

    # Get airport list from controller
    airport_options = [
        Option(f"{airport.name} ({airport.code})", value=airport.code)
        for airport in controller.airports  # Replace with `controller.airports` if you have a list
    ]

    # Get today's date for min attribute on date input
    today = datetime.now().strftime("%Y-%m-%d")

    # Add JavaScript for validation
    validation_script = Script("""
        function validateForm() {
            const origin = document.getElementById('origin').value;
            const destination = document.getElementById('destination').value;
            const date = document.getElementById('flight-date').value;
            const today = new Date().toISOString().split('T')[0];
            
            // Reset error messages
            document.getElementById('same-airports-error').style.display = 'none';
            document.getElementById('past-date-error').style.display = 'none';
            
            // Check if origin and destination are the same
            if (origin === destination) {
                document.getElementById('same-airports-error').style.display = 'block';
                return false;
            }
            
            // Check if date is in the past
            if (date < today) {
                document.getElementById('past-date-error').style.display = 'block';
                return false;
            }
            
            return true;
    }
    """)

    origin = Select(*airport_options, name="origin", id="origin", required=True)
    destination = Select(*airport_options, name="destination", id="destination", required=True)
    date = Input(type="date", name="date", id="flight-date", min=today, required=True)
    submit = Button("Search", type="submit", cls="search-btn")

    return Title("Search Flights"), styles, validation_script, Div(
        H1("Find a Flight"),
        Form(
            Div(Label("From:"), origin),
            Div(id="same-airports-error", cls="error-message", 
                children=["Origin and destination cannot be the same."]),
            Div(Label("To:"), destination),
            Div(Label("Date:"), date),
            Div(id="past-date-error", cls="error-message", 
                children=["Please select a date in the future."]),
            submit,
            action="/search_results",
            method="post",
            cls="form-container",
            onsubmit="return validateForm()"
        ),
        Form(
            Div(
                Button("Go Back", type="submit", style="font-size: 16px; background-color: grey; padding: 10px; border-radius: 8px;", formaction="/home"),
                style="text-align: center; margin-top: -40px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);"
            )
        )
    )

@rt("/search_results", methods=["POST"])
async def search_results(request):
    form_data = await request.form()

    origin_code = form_data.get("origin", "").strip()
    destination_code = form_data.get("destination", "").strip()
    date = form_data.get("date", "").strip()

    try:
        search_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return Div("Invalid date format!", cls="error")

    matching_flights = [
        flight for flight in controller.flights
        if flight.origin == origin_code
        and flight.destination == destination_code
        and datetime.strptime(flight.departure_time, "%Y-%m-%d %H:%M") >= search_date
    ]

    if not matching_flights:
        return Title("Search Results"), Div(
            Div("No flights found!", cls="results-container"),
            Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")
        )

    flight_cards = [
        Div(
            H3(f"{flight.origin} ✈ {flight.destination}", style="color: #F9D01C;"),
            P(f"Departure: {flight.departure_time}"),
            P(f"Arrival: {flight.arrive_time}"),
            P(f"Aircraft: {flight.plane.aircraft}"),
            Form(
                Hidden(name="flight_id", value=flight.flight_id),  # ✅ Store flight ID
                Button("Book This Flight", type="submit", cls="book-btn", formaction="/seat_map")  # ✅ Now goes to /seat_map
            ),
            cls="flight-card"
        )
        for flight in matching_flights
    ]

    styles = Style("""
        body { font-family: Arial, sans-serif; background-color: #000000; color: #333;
               display: flex; flex-direction: column; align-items: center;
               justify-content: center; min-height: 100vh; margin: 0; padding: 20px; }
        .results-container { background: white; padding: 20px; border-radius: 10px;
                             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); width: 90%; max-width: 600px;
                             text-align: center; }
        .flight-card { border: 2px solid #F9D01C; border-radius: 10px;
                       padding: 15px; margin: 10px 0; text-align: left; }
        .book-btn { background-color: #F9D01C; padding: 10px; font-size: 16px;
                    border: none; border-radius: 8px; font-weight: bold;
                    cursor: pointer; transition: 0.3s ease; width: 100%; }
        .book-btn:hover { background-color: #FFD700; }
        .back-btn { background-color: #ccc; padding: 10px; font-size: 16px;
                    border: none; border-radius: 8px; font-weight: bold;
                    cursor: pointer; transition: 0.3s ease; }
        .back-btn:hover { background-color: #bbb; }
    """)

    return Title("Search Results"), styles, Div(
        H1("Available Flights"),
        Div(*flight_cards, cls="results-container"),
        Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")
    )