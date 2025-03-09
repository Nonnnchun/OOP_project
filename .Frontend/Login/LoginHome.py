from fasthtml.common import *
from LoginHomeBack import *

app, rt = fast_app()


# ================================
#           ROUTES
# ================================

# Welcome Page
@rt('/')
def home():
    # Fullscreen Background with Pastel Gradient and Centering
    background = Style("""
        body { 
            height: 100vh; 
            margin: 0;
            font-family: 'Arial', sans-serif;
            color: #555; /* Light text color */
            text-align: center;
            background-image: url('/Picture/fu7.jpg'); /* Add your background image */
            background-size: cover;
            background-position: center;
            background-attachment: cover;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center; /* Horizontally center */
            align-items: center; /* Vertically center */
        }
    """)

    go_to_login = Form(Button("Go to Login Page", 
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
        
        action="/login", 
        method="get",
    )

    return Title("Welcome to my Page"), background, go_to_login

# Registration Page
@rt("/register")
def get():
    return Container(
        H1("Register"),
        Form(
            Label("Email:", Input(name="email", type="email", required=True)),
            Label("Password:", Input(name="password", type="password", required=True)),
            Label("First Name:", Input(name="firstname", required=True)),
            Label("Last Name:", Input(name="lastname", required=True)),
            Button("Register", type="submit"),
            method="post",
            action="/register"
        )
    )

@rt("/register")
def post(email: str, password: str, firstname: str, lastname: str):
    message = controller.register(email, password, firstname, lastname)
    return RedirectResponse('/login', status_code=303) if "successful" in message else message

# Login Page
@rt("/login")
def get():
    return Container(
        H1("Login", style="text-align: center;"),
        Form(
            Label("Email:", Input(name="email", type="email", required=True), style="display: block;"),
            Label("Password:", Input(name="password", type="password", required=True), style="display: block;"),
            A("Don't have an account? Register here!",
            style="""
            display: block;
            text-align: center;
            font-family: 'Arial', sans-serif;
            color: #555; /* Light text color */
            margin-bottom: 10px;
            """ ,
            href="/register"),
            
            Button("Login", type="submit", style="display: block; margin: 0 auto;"),
            method="post",
            action="/login"
        )
    )

@rt("/login")
def post(email: str, password: str):
    message = controller.login(email, password)
    return RedirectResponse('/home', status_code=303) if "success" in message else Container(
        P(message), 
        Form(Button("Return to Login Page", 
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
        
        formaction="/login")
    )

# Home Page (Only Accessible if Logged In)
@rt("/home")
def get():
    user = controller.get_logged_in_user()
    if not user:
       return RedirectResponse('/login', status_code=303)

    return Container(
        H1(f"Hello {user.userdetail.firstname} {user.userdetail.lastname}", 
           style="text-align: center; color: #FFFFFF; margin: 20px 0;"),
        H6(f"Total points: {user.userdetail.points}", 
           style="text-align: center; color: #FFFFFF; margin: 20px 0;"),

        # Grid for cards
        Div(
            Card(
                H3("Find & Book", style="color: #ffee63;"),
                P("Find a flight"),
                Form(Button("Edit", type="submit", formaction="/flight_search")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            
            Card(
                H3("View profile", style="color: #ffee63;"),
                P("View my personal details"),
                Form(Button("Edit", type="submit", formaction="/profile")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            Card(
                H3("My bookings", style="color: #ffee63;"),
                P("View all booked flights"),
                Form(Button("View", type="submit", formaction="/booking")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            Card(
                H3("Promocode", style="color: #ffee63;"),
                P("View all of my promocodes"),
                Form(Button("View", type="submit", formaction="/promocode")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            Card(
                H3("Change password", style="color: #ffee63;"),
                P("New pass, new security"),
                Form(Button("Change", type="submit", formaction="/password")),
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; width: 250px;"
            ),
            style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px;"
        ),

        # Logout button at bottom
        Form(Button("Logout", type="submit", 
                    style="position: fixed; bottom: 20px; right: 20px;", formaction="/logout"))
    )

@rt("/profile")
def get():
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    return Container(
        H1("My Profile", style="text-align: center; color: #FFFFFF; margin: 20px 0;"),
        
        Card(
            H3("Profile Information", style="color: #ffee63;"),
            P(f"Name: {user.userdetail.firstname} {user.userdetail.lastname}"),
            P(f"Birthday: {user.userdetail.birthday}"),
            P(f"Gender: {user.userdetail.gender}"),
            P(f"Nationality: {user.userdetail.nationality}"),
            P(f"Phone: {user.userdetail.phone_number}"),
            P(f"Address: {user.userdetail.address}"),
            Form(
                Button("Edit", style="background-color: #ffee63; padding: 10px; font-size: 16px;", 
                    formaction="/edit-profile")
            ),
            
            Form(
                Button("Back", style="background-color: #ccc; padding: 10px; font-size: 16px;", 
                    formaction="/home")
            ),
            
            id="profile-card",
            style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
        ),
    )

@rt("/edit-profile", methods=["GET", "POST"])
def edit_profile(lastname: str = "", phone_number: str = "", address: str = ""):
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)
    
    if lastname or phone_number or address:  
        user.userdetail.edit_profile(lastname=lastname, phone_number=phone_number, address=address)

        # After saving, show the updated profile card
        return Card(
            H3("Profile Information", style="color: #ffee63;"),
            P(f"Name: {user.userdetail.firstname} {user.userdetail.lastname}"),
            P(f"Birthday: {user.userdetail.birthday}"),
            P(f"Gender: {user.userdetail.gender}"),
            P(f"Nationality: {user.userdetail.nationality}"),
            P(f"Phone: {user.userdetail.phone_number}"),
            P(f"Address: {user.userdetail.address}"),
            Form(
                Button("Edit", style="background-color: #ffee63; padding: 10px; font-size: 16px;", 
                    formaction="/edit-profile")
            ),
            
            Form(
                Button("Back", style="background-color: #ccc; padding: 10px; font-size: 16px;", 
                    formaction="/home")
            ),
            id="profile-card",
            style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
        )

    # Show the edit form
    return Card(
        H3("Edit Profile", style="color: #ffee63;"),
        Form(
            Label("Last Name"),
            Input(name="lastname", type="text", value=user.userdetail.lastname),
            
            Label("Phone Number"),
            Input(name="phone_number", type="text", value=user.userdetail.phone_number),
            
            Label("Address"),
            Input(name="address", type="text", value=user.userdetail.address),
            
            Button("Save Changes", type="submit", 
                hx_post="/edit-profile", 
                hx_target="#profile-card", 
                hx_swap="outerHTML",
                style="background-color: #ffee63; padding: 10px; font-size: 16px;"
            ),
            method="post",
            style="display: flex; flex-direction: column; gap: 10px;"
        ),
        id="profile-card",
        style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
    )
    
@rt("/password", methods=["GET", "POST"])
def get():
    return Container(
        H2("Change Your Password", style="text-align: center; color: #fff; margin: 20px 0;"),

        # Password change form
        Form(
            Input(name="old_password", type="password", placeholder="Enter old password", required=True),
            Input(name="new_password", type="password", placeholder="Enter new password", required=True),
            Input(name="confirm_new_password", type="password", placeholder="Confirm new password", required=True),

            # Submit button
            Button("Submit", type="submit", style="font-size: 16px; background-color: #ffee63; padding: 10px;",
                   formaction="/passwordCheck"),
            style="text-align: center; padding: 20px; display: flex; flex-direction: column; gap: 10px;"
        ),

        # Separate Go Back button (not inside the form to prevent validation issues)
        Form(
            Button("Go Back", type="submit", style="font-size: 16px; background-color: #ccc; padding: 10px;",
                   formaction="/home"),
            style="text-align: center; margin-top: -40px; padding: 20px;"  # Moves the button closer to the form
        )
    )
     
@rt("/passwordCheck", methods=["GET","POST"])
def password_change(old_password: str = "", new_password: str = "", confirm_new_password: str = ""):
    user = controller.get_logged_in_user()  # Get the logged-in user
    if not user:
        return RedirectResponse('/login', status_code=303)

    result = user.change_password(old_password, new_password, confirm_new_password)

    color = "green" if "successfully" in result else "red"
    if "successfully" in result:
        controller.logout()
        return Container(H3(result, style=f"color: {color}; text-align: center;"),
                    Form(Button("Go Back to login page", type="submit", style="font-size: 16px; background-color: #ccc; padding: 10px;",
                    formaction="/logout")
                     )
        )
    else :
        return Container(H3(result, style=f"color: {color}; text-align: center;"),
                    Form(Button("Try again", type="submit", style="font-size: 16px; background-color: #ccc; padding: 10px;",
                    formaction="/password")
                    )
        )
# Logout
@rt("/logout")
def get():
    controller.logout()
    return RedirectResponse('/login', status_code=303)

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
        ),
        Form(
            Div(
                Button("Go Back", type="submit", style="font-size: 16px; background-color: grey; padding: 10px; border-radius: 8px;",
                formaction="/home"),
            style="text-align: center; margin-top: -40px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);"
    )
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