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
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    return Container(
        H1(f"Welcome, {user.userdetail.firstname} {user.userdetail.lastname}!"),
        P(f"Your total points: {user.userdetail.points}"),
        Grid(
            Card(
                H3("Profile"),
                P("View your personal details"),
                Form(Button("View Profile", formaction="/profile", type="submit"))
            ),
            Card(
                H3("Logout"),
                Form(Button("Logout", formaction="/logout", type="submit"))
            )
        )
    )

@rt("/profile")
def get():
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    return Container(
        H1("Your Profile"),
        P(f"Name: {user.userdetail.firstname} {user.userdetail.lastname}"),
        P(f"Email: {user.email}"),
        P(f"Points: {user.userdetail.points}"),
        Form(Button("Back to Home", formaction="/home", type="submit"))
    )

# Logout
@rt("/logout")
def get():
    controller.logout()
    return RedirectResponse('/login', status_code=303)


serve()