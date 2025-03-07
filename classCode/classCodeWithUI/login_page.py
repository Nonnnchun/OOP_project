from fasthtml.common import *

app, rt = fast_app()

class Controller:
   def __init__(self):
      self.plane_list = []
      self.account_list = []
      self.flightRoute_list = []
      self.is_logged_in = False

   def turn_into_system(self, account):
      # Check if the account is registered (has account)
      if not account.has_account():
         account.register()  # Register the user
         if account.is_success():
               return "Registration successful"
         return self.auto_path_to_login(account)
      else:
         account.login()  # Login if the account exists
         if account.is_correct():
               self.is_logged_in = True
               return "Login successful"

   def auto_path_to_login(self, account):
      # Auto login if the user is not registered
      account.login()
      if account.is_correct():
         self.is_logged_in = True
         return "Login successful"

   def display_home_page(self):
      print("Displaying home page")

   def flight_search(self):
      destination = input("Enter destination: ")
      date = input("Enter date (YYYY-MM-DD): ")
      available_flights = [flight for flight in self.flightRoute_list if flight.destination == destination and flight.date == date]
      if available_flights:
         print("Available flights:")
         for flight in available_flights:
               print(f"Flight ID: {flight.id}, Departure: {flight.departure_time}, Arrival: {flight.arrival_time}")
      else:
         print("No flights available for the given destination and date.")


class Account:
   def __init__(self, email, password):
      self.email = email
      self.password = password
      self.purchased_history = []
      self.userdetail = None  # Holds details of user (points, promo codes, etc.)

   def login(self):
      print("Login Page")
      # Implement login logic here
   
   def register(self, email, password, userdetail):
      print("Registering user")
      self.email = email
      self.password = password
      self.userdetail = userdetail  # The UserDetail object (which holds points, promo codes, etc.)
   
   def forgot_pass(self):
      print("Forgot Password Page")
      # Implement forgot password logic here
   
   def is_correct(self):
      # Placeholder for actual validation logic
      # You can compare credentials or any other validation here
      return True
   
   def is_success(self):
      # Check if registration was successful
      return True

   def return_home_page(self):
      print("Returning Home Page")
   
   def has_account(self):
      # Check if account is registered by ensuring both email and password are set
      return bool(self.email and self.password)
   
   def change_password(self, old_password, new_password, confirm_new_password):
      if old_password != self.password:
         return "Old password is incorrect"
      if new_password != confirm_new_password:
         return "New passwords do not match"
      if len(new_password) < 6:  # Ensure new password is strong
         return "New password must be at least 6 characters long"
      
      self.password = new_password
      return "Password changed successfully"
   
   def logout(self):
      print("Logging out...")
      # Implement logout logic here


class UserDetail:
   def __init__(self, points, promocode):
      self.points = points
      self.promocode = promocode

   def get_promocode(self):
      return self.promocode

# Example usage

# Create a UserDetail object with points and a promo code
user_detail = UserDetail(points=100, promocode="DISCOUNT10")

# Create an Account object with email, password, and UserDetail
account = Account(email="user@example.com", password="password123")

# Register the user
account.register(email="user@example.com", password="password123", userdetail=user_detail)

# Create a Controller object and manage the system
controller = Controller()
print(controller.turn_into_system(account))

# Check if user is logged in and display home page
if controller.is_logged_in:
   controller.display_home_page()

# Flight search
controller.flight_search()



@rt('/login')
def get():
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

   # Header with Circular Logo and Pastel Styling
   header = Div(
      Img(src="/Picture/fu4.jpg", style="height: 50px; width: 50px; border-radius: 50%; object-fit: cover; margin-right: 10px;"),
      "Shit-Airline",
      style="padding: 15px; font-weight: bold; font-size: 24px; display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; background-color: rgba(255, 255, 255, 0.7);"
   )

   # Login form with Acrylic (Glassmorphism) Effect and Pastel Details
   login_form = Form(
      H2("Login", style="color: #6C4F82; margin-bottom: 20px; font-weight: bold;"),  # Pastel purple

      # Input fields with pastel and glassmorphism effect
      Input(id="username", placeholder="ชื่อผู้ใช้", required=True, 
            style="width: 100%; padding: 12px; margin: 10px 0; border: none; border-radius: 100px; background: rgba(255, 255, 255, 0.5); color: #6C4F82; backdrop-filter: blur(10px);"),
      Input(id="password", type="password", placeholder="รหัสผ่าน", required=True, 
            style="width: 100%; padding: 12px; margin: 10px 0; border: none; border-radius: 8px; background: rgba(255, 255, 255, 0.5); color: #6C4F82; backdrop-filter: blur(10px);"),
      
      # Login button with pastel yellow color
      Button("เข้าสู่ระบบ", 
            style="background-color: #FFEB99; color: #333; width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s ease; border: 2px solid #F9D01C;",
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
      
      action="/login", method="post",
      style="background: rgba(255, 255, 255, 0.7); padding: 30px; border-radius: 12px; box-shadow: 0px 10px 24px rgba(60, 50, 50, 0.3); max-width: 400px; width: 100%; text-align: center; backdrop-filter: blur(20px); border: 1px solid rgba(60, 50, 50, 0.2);"
   )

   # Register link with pastel hover effect
   register_link = P(
      A("ลงทะเบียน", href="/registration", 
      style="color: #F9D01C; text-decoration: none; font-size: 14px; margin-top: 15px; display: inline-block; transition: 0.3s ease; font-weight: bold;",
      onmouseover="this.style.color='#FFD700'",
      onmouseout="this.style.color='#F9D01C'")
   )

   # Centering Everything
   content = Div(
      header,
      Div(login_form, register_link, style="margin-top: 40px;"),
      style="display: flex; flex-direction: column; align-items: center; width: 100%;"
   )




@rt("/registration")
def get():
   return Container(
      H1("Registration Form"),
      Form(
         # Personal Details
         Group(
            H3("Personal Information"),
            Label("Username:", Input(type="text", id="username", required=True)),
            Label("Password:", Input(type="password", id="password", required=True)),
            Label("Email:", Input(type="email", id="email", required=True)),
            Label("Age:", Input(type="number", id="age", min="18", max="100"))
         ),
         
         # Gender Selection
         Group(
            H3("Gender"),
            Label(Input(type="radio", name="gender", value="male"), "Male"),
            Label(Input(type="radio", name="gender", value="female"), "Female"),
            Label(Input(type="radio", name="gender", value="other"), "Other")
         ),

         # Country Selection
         Group(
            H3("Location"),
            Label("Country:",
               Select(
                  Option("USA", value="usa"),
                  Option("UK", value="uk"),
                  Option("Thailand", value="th"),
                  id="country"
               )
            )
         ),
         
         # Terms Agreement
         Group(
            Label(CheckboxX(id="agree", label="I agree to the terms", required=True))
         ),

         Button("Register", type="submit", style="background-color: #FFEB99; color: #333; width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s ease; border: 2px solid #F9D01C;",
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
         method="post",
         action="/register"
      )
   )

@rt("/register")
def post():
   return Container(
      H1("Registration Successful"),
      P("Thank you for registering!"),
      Button("Return to login page", type="submit", style="background-color: #FFEB99; color: #333; width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s ease; border: 2px solid #F9D01C;",
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
         method="post",
         action="/login"
   )

@rt("/profile")
def get():
   return Container(
      H1("Profile Form"),
      Form(
         # Personal Information
         Group(
            H3("Personal Information"),
            Label("First Name:", Input(type="text", id="firstname")),
            Label("Last Name:", Input(type="text", id="lastname")),
            Label("Birth Date:", Input(type="date", id="birthdate"))
         ),
         
         # Contact Information
         Group(
            H3("Contact Information"),
            Label("Email:", Input(type="email", id="email")),
            Label("Phone:", Input(type="tel", id="phone")),
            Label("Address:", Textarea(id="address", rows=3))
         ),
         
         Button("Save Profile", type="submit", style="background-color: #FFD100; border: none; padding: 10px; border-radius: 5px;"),
         method="post",
         action="/save-profile"
      )
   )

@rt("/save-profile")
def post():
   return Container(
      H1("Profile Saved"),
      P("Your profile has been saved successfully!")
   )

@rt("/login")
def post():
   return Container(
      H1("Registration Successful"),
      P("Thank you for registering!"),
      Button("Return to login page", type="submit", style="background-color: #FFEB99; color: #333; width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s ease; border: 2px solid #F9D01C;",
            onmouseover="this.style.backgroundColor='#F9D01C'",
            onmouseout="this.style.backgroundColor='#FFEB99'"),
         method="post",
         action="/profile"
   )

serve()