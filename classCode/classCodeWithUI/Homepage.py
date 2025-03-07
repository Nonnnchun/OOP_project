from fasthtml.common import *

class Controller:
    def __init__(self):
        self.plane_list = []
        self.account_list = []
        self.flightRoute_list = []

    def flight_search(self):
        pass

    def get_user_acc(self):
        pass

class Seat:
    def __init__(self, seat_id, seat_type):
        self.seat_id = seat_id
        self.seat_type = seat_type

class Airport:
    def __init__(self, name):
        self.name = name

class Plane:
    def __init__(self, plane_id, aircraft, seats):
        self.plane_id = plane_id
        self.aircraft = aircraft
        self.seats = seats

class FlightRoute:
    def __init__(self, origin, destination, departure_time, arrive_time):
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrive_time = arrive_time

class Booking:
    def __init__(self, booking_reference, payment, status, flight, passenger_details, promocode_discount, price, luggage):
        self.booking_reference = booking_reference
        self.payment = payment
        self.status = status
        self.flight = flight
        self.passenger_details = passenger_details
        self.promocode_discount = promocode_discount
        self.price = price
        self.luggage = luggage

    def edit_booking(self):
        pass

    def price_cal(self):
        pass

class Luggage:
    def __init__(self, kilogram, price_rate):
        self.kilogram = kilogram
        self.price_rate = price_rate

class Payment:
    def __init__(self, ticket_price, amount):
        self.ticket_price = ticket_price
        self.amount = amount

    def process_payment(self):
        pass

class PaymentMethod:
    def __init__(self):
        pass

class OnlineBanking(PaymentMethod):
    def __init__(self):
        super().__init__()

class Account:
    def __init__(self, password, email, purchased_history, user_detail):
        self.password = password
        self.email = email
        self.purchased_history = purchased_history
        self.user_detail = user_detail

    def login(self):
        pass

    def register(self):
        pass

    def forgot_pass(self):
        pass

    def get_booking_list(self):
        return []

    def get_promocode(self):
        return self.user_detail.get_promocode()

    def use_points(self, points):
        if self.user_detail.point >= points:
            self.user_detail.point -= points
            return True
        return False

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
        pass

class UserDetail:
    def __init__(self, firstname, lastname, birthday, gender, identification, nationality, phone_number, address, point, promocode_list):
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.gender = gender
        self.identification = identification
        self.nationality = nationality
        self.phone_number = phone_number
        self.address = address
        self.point = point
        self.promocode_list = promocode_list

    def edit_profile(self, firstname=None, lastname=None, phone_number=None, address=None):
        if firstname:
            self.firstname = firstname
        if lastname:
            self.lastname = lastname
        if phone_number:
            self.phone_number = phone_number
        if address:
            self.address = address

    def get_promocode(self):
        return self.promocode_list
    
    def get_user_detail(self):
        return [
            self.firstname,
            self.lastname,
            self.birthday,
            self.gender,
            self.identification,
            self.nationality,
            self.phone_number,
            self.address,
            self.point,
            self.promocode_list
        ] 

class Promocode:
    def __init__(self, code, point, discount_percent, expiration_date):
        self.code = code
        self.point_to_use = point
        self.discount_percent = discount_percent
        self.expiration_date = expiration_date

    def is_valid(self):
        return True

# Mockup Data
seat1 = Seat("1A", "Economy")
plane1 = Plane("P001", "Boeing 737", [seat1])
flight1 = FlightRoute("JFK", "LAX", "10:00", "13:00")
promocode1 = Promocode("DISCOUNT10", 10, 5, "2025-12-31")
promocode2 = Promocode("SALE20", 20, 5,"2025-06-30")
user_detail1 = UserDetail("John", "Dejavu", "1990-05-15", "Male", "123456789", "USA", "555-1234", "123 Main St", 100, [promocode1, promocode2])
account1 = Account("password123", "john.doe@example.com", [], user_detail1)
controller = Controller()
controller.account_list.append(account1)

# Fetching user details from mock data
user_firstname = controller.account_list[0].user_detail.firstname
user_lastname = controller.account_list[0].user_detail.lastname
user_points = controller.account_list[0].user_detail.point
account = controller.account_list[0]
# FastHTML app
app, rt = fast_app()

@rt("/")
def get():
    user = controller.account_list[0].user_detail
    return Container(
        
        H1(f"Hello {user.firstname} {user.lastname}", style="text-align: center; color: #FFFFFF; margin: 20px 0;"),
        H6(f"Total point : {user.point}", style="text-align: center; color: #FFFFFF; margin: 20px 0;"),
        
        Grid(
            # Card 1 พาเช้าไปหน้า edit profile
            Card(
                H3("View profile", style="color: #ffee63;"),
                P("View my personal detail", 
                style="text-align: left; font-size: 16px; line-height: 1.5;"),
                Form(
                    Button("Edit", type="submit", style="text-align: center; font-size: 16px; line-height: 1.5;", 
                        formaction="/Viewprofile"),
                ),
                style=""" 
                    border: 2px solid #fef5f3;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                """
            ),

            # Card 2 แสดง ิbooking ที่เคยทำมาทั้งหมด (addition : อาจจะใส่พวกอันที่ book ไว้้แล้วยังไม่ชำระเงินไว้ในนี้ด้วย)
            Card(
                H3("My bookings ", style="color: #ffee63;"),
                P("View my all booked flight"),
                P(" "),
                Form(
                    Button("View", type="submit", style="text-align: center; font-size: 16px; line-height: 1.5;", 
                        formaction="/booking"),
                ),
                style="""
                    border: 2px solid #fef5f3;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                """
            ),

            # Card 3 ไปต่อหน้ารวม promo code ที่มี
            Card(
                H3("Promocode", style="color: #ffee63;"),
                P("View all of my promocode "),
                Form(
                    Button("View", type="submit", style="text-align: center; font-size: 16px; line-height: 1.5;", 
                        formaction="/promocode"),
                ),
                style="""
                    border: 2px solid #fef5f3;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                """
            ),

            # Card ที่ 4 - แสดงการจัดการ margin และ padding
            Card(
                H3("Change password", style="color: #ffee63;"),
                P("New pass new secure"),
                Form(
                    Button("Change", type="submit", style="text-align: center; font-size: 16px; line-height: 1.5;", 
                        formaction="/password"),
                ),
                style="""
                    border: 2px solid #fef5f3;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px;
                """
            )
        ),

    )
    
@rt("/password", methods=["GET", "POST"])
def get():

    return Container(
        H2("Change Your Password", style="text-align: center; color: #fff; margin: 20px 0;"),
        Form(
            Input(name="old_password", type="password", placeholder="Enter old password", required=True),
            Input(name="new_password", type="password", placeholder="Enter new password", required=True),
            Input(name="confirm_new_password", type="password", placeholder="Confirm new password", required=True),
            Button("Submit", type="submit", style="font-size: 16px; line-height: 1.5; background-color: #ffee63; padding: 10px;",
            formaction="/passwordCheck"),
            style="text-align: center; padding: 20px;"
        )
    )
    
@rt("/passwordCheck", methods=["GET","POST"])
def password_change(old_password: str = "", new_password: str = "", confirm_new_password: str = ""):
    result = account.change_password(old_password, new_password, confirm_new_password)

    color = "green" if "successfully" in result else "red"
    return Container(H3(result, style=f"color: {color}; text-align: center;"))

@rt("/Viewprofile", methods=["GET"])
def profile():
    user = controller.account_list[0].user_detail  # Get user details
    
    return Container(
        H1("My Profile", style="text-align: center; color: #FFFFFF; margin: 20px 0;"),
        
        Card(
            H3("Profile Information", style="color: #ffee63;"),
            P(f"Name: {user.firstname} {user.lastname}"),
            P(f"Birthday: {user.birthday}"),
            P(f"Gender: {user.gender}"),
            P(f"Nationality: {user.nationality}"),
            P(f"Phone: {user.phone_number}"),
            P(f"Address: {user.address}"),
            Form(
                Button("Edit", style="background-color: #ffee63; padding: 10px; font-size: 16px;", 
                    formaction="/edit-profile")
            ),
            
            Form(
                Button("Back", style="background-color: #ccc; padding: 10px; font-size: 16px;", 
                    formaction="/")
            ),
            
            id="profile-card",
            style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
        ),
    )

@rt("/edit-profile", methods=["GET", "POST"])
def edit_profile(lastname: str = "", phone_number: str = "", address: str = ""):
    user = controller.account_list[0].user_detail  # Get user details
    
    if lastname or phone_number or address:  # If form is submitted
        user.edit_profile(lastname=lastname, phone_number=phone_number, address=address)

        # After saving, show the updated profile card
        return Card(
            H3("Profile Information", style="color: #ffee63;"),
            P(f"Name: {user.firstname} {user.lastname}"),
            P(f"Birthday: {user.birthday}"),
            P(f"Gender: {user.gender}"),
            P(f"Nationality: {user.nationality}"),
            P(f"Phone: {user.phone_number}"),
            P(f"Address: {user.address}"),
            Form(
                Button("Edit", style="background-color: #ffee63; padding: 10px; font-size: 16px;", 
                    formaction="/edit-profile")
            ),
            
            Form(
                Button("Back", style="background-color: #ccc; padding: 10px; font-size: 16px;", 
                    formaction="/")
            ),
            id="profile-card",
            style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
        )

    # Show the edit form
    return Card(
        H3("Edit Profile", style="color: #ffee63;"),
        Form(
            Label("Last Name"),
            Input(name="lastname", type="text", value=user.lastname),
            
            Label("Phone Number"),
            Input(name="phone_number", type="text", value=user.phone_number),
            
            Label("Address"),
            Input(name="address", type="text", value=user.address),
            
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


@rt("/booking", methods=["GET", "POST"])
def get():
    return

@rt("/promocode", methods=["GET", "POST"])
def get():
    return

serve()