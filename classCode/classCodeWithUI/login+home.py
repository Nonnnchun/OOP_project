from fasthtml.common import *
from hmac import compare_digest

app, rt = fast_app()

# ================================
#   ACCOUNT MANAGEMENT CLASSES
# ================================
class UserDetail:
    def __init__(self, firstname, lastname, points=0):
        self.firstname = firstname
        self.lastname = lastname
        self.points = points

class Account:
    def __init__(self, email, password, userdetail):
        self.email = email
        self.password = password
        self.userdetail = userdetail

    def check_password(self, password):
        return compare_digest(self.password, password)

# Controller to manage users
class Controller:
    def __init__(self):
        self.accounts = []  # List of registered accounts
        self.logged_in_user = None  # Store currently logged-in user

    def register(self, email, password, firstname, lastname):
        if any(acc.email == email for acc in self.accounts):
            return "Email already registered!"
        
        user_detail = UserDetail(firstname, lastname)
        new_account = Account(email, password, user_detail)
        self.accounts.append(new_account)
        return "Registration successful!"

    def login(self, email, password):
        for acc in self.accounts:
            if acc.email == email and acc.check_password(password):
                self.logged_in_user = acc
                return "Login successful!"
        return "Invalid email or password!"

    def get_logged_in_user(self):
        return self.logged_in_user

    def logout(self):
        self.logged_in_user = None

controller = Controller()

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
    
    go_to_login = Form(Button("เข้าสู่ระบบ", 
            style="background-color: #FFEB99; color: #333; width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s ease; border: 2px solid #F9D01C;",
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
        
        action="/login", method="post",
        style="background: rgba(255, 255, 255, 0.7); padding: 30px; border-radius: 12px; box-shadow: 0px 10px 24px rgba(60, 50, 50, 0.3); max-width: 400px; width: 100%; text-align: center; backdrop-filter: blur(20px); border: 1px solid rgba(60, 50, 50, 0.2);"
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
        H1("Login"),
        Form(
            Label("Email:", Input(name="email", type="email", required=True)),
            Label("Password:", Input(name="password", type="password", required=True)),
            Button("Login", type="submit"),
            method="post",
            action="/login"
        )
    )

@rt("/login")
def post(email: str, password: str):
    message = controller.login(email, password)
    return RedirectResponse('/home', status_code=303) if "successful" in message else message

# Home Page (Only Accessible if Logged In)
@rt("/home")
def get():
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

# Profile Page
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

# Run FastHTML App
serve()
