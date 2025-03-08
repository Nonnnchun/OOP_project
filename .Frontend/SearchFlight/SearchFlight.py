from fasthtml.common import *
from hmac import compare_digest
from SearchFlightBack import *

app, rt = fast_app()


@rt('/')
def home():
    go_to_serch = Form(Button("flight search", 
            style="""background-color: #FFEB99;
            color: #333; width: 100%; 
            padding: 12px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            transition: 0.3s ease; 
            border: 2px solid #F9D01C;""",
            
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
            
            action="/flight_search", 
            method="get",
        )
    return Title("Welcome to my Page"), go_to_serch


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
            background-color: #fff;
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
    """)

    # Correcting Select dropdowns
    origin = Select(
        Option("Bangkok"),
        Option("Chiang Mai"),
        Option("Phuket"),
        Option("Hat Yai"),
        name="origin",
        required=True
    )

    destination = Select(
        Option("Bangkok"),
        Option("Chiang Mai"),
        Option("Phuket"),
        Option("Hat Yai"),
        name="destination",
        required=True
    )

    date = Input(type="date", name="date", required=True)
    submit = Button("Search", type="submit", cls="search-btn")

    return Title("Search Flights"), styles, Div(
        H1("Find a Flight"),
        Form(
            Div(Label("From:"), origin),
            Div(Label("To:"), destination),
            Div(Label("Date:"), date),
            submit,
            action="/search_results",
            method="post",
            cls="form-container"
        )
    )

@rt("/search_results", methods=["POST"])
async def search_results(request):  # ✅ Make function async to handle form extraction
    form_data = await request.form()  # ✅ Correct way to get form data

    origin = form_data.get("origin", "").strip()
    destination = form_data.get("destination", "").strip()
    date = form_data.get("date", "").strip()

    # Debugging print statements
    print(f"Received Origin: '{origin}', Destination: '{destination}', Date: '{date}'")

    # Fetch matching flights from the controller
    matching_flights = [
        flight for flight in controller.flights
        if flight.origin.strip().lower() == origin.lower()
        and flight.destination.strip().lower() == destination.lower()
        and flight.date.strip() == date
    ]

    # Print all flights in the controller to check if the desired one exists
    print("All flights in controller:")
    for flight in controller.flights:
        print(f"ID: {flight.id}, From: {flight.origin}, To: {flight.destination}, Date: {flight.date}, Price: {flight.price}, Available: {flight.available}")

    # Print matching flights found
    print("Matching flights found:")
    for flight in matching_flights:
        print(f"ID: {flight.id}, From: {flight.origin}, To: {flight.destination}, Date: {flight.date}, Price: {flight.price}, Available: {flight.available}")
    print(f"Received Origin: '{origin}', Destination: '{destination}', Date: '{date}'")
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #000000;
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .results-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 600px;
            text-align: center;
        }
        .flight-card {
            border: 2px solid #F9D01C;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            text-align: left;
        }
        .back-btn {
            background-color: #ccc;
            padding: 10px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
        }
        .back-btn:hover {
            background-color: #ccc;
        }
    """)

    if not matching_flights:
        return Title("Search Results"), styles, Div(
            Div("No flights found!", cls="results-container"),
            Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")
        )

    flight_cards = [
        Div(
            H3(f"{flight.origin} ✈ {flight.destination}", style="color: #F9D01C;"),
            P(f"Date: {flight.date}"),
            P(f"Price: {flight.price} THB"),
            P(f"Available: {'✅ Yes' if flight.available else '❌ No'}"),
            cls="flight-card"
        )
        for flight in matching_flights
    ]

    return Title("Search Results"), styles, Div(
        H1("Available Flights"),
        Div(*flight_cards, cls="results-container"),
        Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")
    )

serve()