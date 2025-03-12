from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app(hdrs=(Script("https://unpkg.com/htmx.org@1.9.6", defer=True),))
home_app = app 

@rt("/home")
def get():
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    menu_styles = Style("""
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-image: url('/Picture/fu7.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            color: #fff;
        }
        .overlay {
            background-color: rgba(0, 0, 0, 0.5);
            min-height: 100vh;
            width: 100%;
            padding: 30px 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .welcome-card {
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .welcome-header {
            color: #fff;
            margin-bottom: 15px;
            font-size: 28px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .points-display {
            color: rgba(255, 255, 255, 0.9);
            font-size: 18px;
            margin-bottom: 0;
        }
        .points-value {
            color: #4fc3f7;
            font-weight: bold;
            font-size: 22px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .menu-container {
            max-width: 450px;
            margin: 0 auto;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .menu-item {
            display: flex;
            align-items: center;
            padding: 18px 25px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            text-decoration: none;
            color: #fff;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .menu-item:last-child {
            border-bottom: none;
        }
        .menu-item:hover {
            background-color: rgba(255, 255, 255, 0.2);
            transform: translateX(5px);
        }
        .menu-item:hover .menu-icon {
            transform: scale(1.2);
        }
        .menu-icon {
            margin-right: 20px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(79, 195, 247, 0.2);
            border-radius: 50%;
            font-size: 18px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        .menu-text {
            font-size: 16px;
            font-weight: 500;
            letter-spacing: 0.5px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }
        .menu-item:nth-child(1) .menu-icon {
            background-color: rgba(156, 39, 176, 0.3);
        }
        .menu-item:nth-child(2) .menu-icon {
            background-color: rgba(33, 150, 243, 0.3);
        }
        .menu-item:nth-child(3) .menu-icon {
            background-color: rgba(0, 188, 212, 0.3);
        }
        .menu-item:nth-child(4) .menu-icon {
            background-color: rgba(121, 85, 72, 0.3);
        }
        .menu-item:nth-child(5) .menu-icon {
            background-color: rgba(63, 81, 181, 0.3);
        }
        .menu-item:nth-child(6) .menu-icon {
            background-color: rgba(233, 30, 99, 0.3);
        }
        .menu-item::after {
            content: '›';
            position: absolute;
            right: 25px;
            font-size: 24px;
            opacity: 0;
            transition: all 0.3s ease;
            color: rgba(255, 255, 255, 0.8);
        }
        .menu-item:hover::after {
            opacity: 1;
            right: 20px;
        }
    """)

    return Div(
        menu_styles,
        Div(
            Div(
                Div(
                    H1(f"Welcome, {user.userdetail.firstname} {user.userdetail.lastname}", cls="welcome-header"),
                    cls="welcome-card"
                ),
                
                Div(
                    A(
                        Div(Span("🎫", cls=""), cls="menu-icon"),
                        Span("My Bookings", cls="menu-text"),
                        href="/manage-booking",
                        cls="menu-item"
                    ),
                    A(
                        Div(Span("✈️", cls=""), cls="menu-icon"),
                        Span("Book flight", cls="menu-text"),
                        href="/flight_search",
                        cls="menu-item"
                    ),
                    A(
                        Div(Span("✏️", cls=""), cls="menu-icon"),
                        Span("Edit Profile", cls="menu-text"),
                        href="/edit-profile",
                        cls="menu-item"
                    ),
                    A(
                        Div(Span("🎟️", cls=""), cls="menu-icon"),
                        Span("Vouchers", cls="menu-text"),
                        href="/promocode",
                        cls="menu-item"
                    ),
                    A(
                        Div(Span("🔒", cls=""), cls="menu-icon"),
                        Span("Change Password", cls="menu-text"),
                        href="/password",
                        cls="menu-item"
                    ),
                    A(
                        Div(Span("🚪", cls=""), cls="menu-icon"),
                        Span("Log Out", cls="menu-text"),
                        href="/logout",
                        cls="menu-item"
                    ),
                    cls="menu-container"
                ),
                cls="container"
            ),
            cls="overlay"
        )
    )

@rt("/profile")
def get():
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    profile_styles = Style("""
        body {
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background-image: url('/Picture/fu4.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            color: #fff;
        }
        .overlay {
            background-color: rgba(0, 0, 0, 0.5);
            min-height: 100vh;
            width: 100%;
            padding: 30px 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .title {
            text-align: center;
            color: #fff;
            margin-bottom: 30px;
            font-size: 32px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .profile-card {
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
        }
        .profile-header {
            color: #4fc3f7;
            margin-bottom: 25px;
            font-size: 24px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding-bottom: 15px;
        }
        .profile-info {
            margin-bottom: 10px;
            font-size: 16px;
            display: flex;
        }
        .profile-label {
            font-weight: bold;
            width: 120px;
            color: rgba(255, 255, 255, 0.9);
        }
        .profile-value {
            flex: 1;
        }
        .button-group {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            gap: 15px;
        }
        .btn {
            padding: 12px 25px;
            border-radius: 30px;
            border: none;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .btn-primary {
            background-color: rgba(33, 150, 243, 0.8);
            color: white;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
        }
        .btn-primary:hover {
            background-color: rgba(33, 150, 243, 1);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
        }
        .btn-secondary {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .btn-secondary:hover {
            background-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
    """)

    return Div(
        profile_styles,
        Div(
            Div(
                H1("My Profile", cls="title"),
                Div(
                    H3("Profile Information", cls="profile-header"),
                    Div(
                        Span("Name:", cls="profile-label"),
                        Span(f"{user.userdetail.firstname} {user.userdetail.lastname}", cls="profile-value"),
                        cls="profile-info"
                    ),
                    Div(
                        Span("Birthday:", cls="profile-label"),
                        Span(f"{user.userdetail.birthday}", cls="profile-value"),
                        cls="profile-info"
                    ),
                    Div(
                        Span("Gender:", cls="profile-label"),
                        Span(f"{user.userdetail.gender}", cls="profile-value"),
                        cls="profile-info"
                    ),
                    Div(
                        Span("Nationality:", cls="profile-label"),
                        Span(f"{user.userdetail.nationality}", cls="profile-value"),
                        cls="profile-info"
                    ),
                    Div(
                        Span("Phone:", cls="profile-label"),
                        Span(f"{user.userdetail.phone_number}", cls="profile-value"),
                        cls="profile-info"
                    ),
                    Div(
                        Span("Address:", cls="profile-label"),
                        Span(f"{user.userdetail.address}", cls="profile-value"),
                        cls="profile-info"
                    ),
                    Div(
                        Form(
                            Button("Edit Profile", cls="btn btn-primary", formaction="/edit-profile"),
                        ),
                        Form(
                            Button("Back to Home", cls="btn btn-secondary", formaction="/home"),
                        ),
                        cls="button-group"
                    ),
                    cls="profile-card"
                ),
                cls="container"
            ),
            cls="overlay"
        )
    )

@rt("/edit-profile", methods=["GET", "POST"])
def edit_profile(firstname: str="", lastname: str="", birthday: str="", phone_number: str="", 
                 address: str="", gender: str="", nationality: str=""):
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)
    
    if firstname or lastname or phone_number or address or birthday or gender or nationality:  
        user.userdetail.edit_profile(
            firstname=firstname, lastname=lastname, phone_number=phone_number, 
            address=address, birthday=birthday, gender=gender, nationality=nationality
        )

        # ✅ Maintain full structure to prevent style issues
        return Div(
            COMMON_STYLES,  # Ensure styles are included in the update
            Div(
                Card(
                    H3("Profile Information", style="color: var(--primary-color); margin-bottom: 1.5rem;"),
                    P(f"Name: {user.userdetail.firstname} {user.userdetail.lastname}"),
                    P(f"Birthday: {user.userdetail.birthday}"),
                    P(f"Gender: {user.userdetail.gender}"),
                    P(f"Nationality: {user.userdetail.nationality}"),
                    P(f"Phone: {user.userdetail.phone_number}"),
                    P(f"Address: {user.userdetail.address}"),
                    Div(
                        Form(Button("Edit", cls="btn btn-primary", formaction="/edit-profile"), style="display: inline-block; margin-right: 1rem;"),
                        Form(Button("Back", cls="btn btn-secondary", formaction="/home"), style="display: inline-block;")
                    ),
                    cls="card"
                ),
                style="margin: 20px auto; max-width: 600px;"  # ✅ Ensures consistent styling
            ),
            id="profile-card"  # Ensure correct target for HTMX update
        )

    # ✅ Show edit form (unchanged)
    return Card(
        H3("Edit Profile", style="color: var(--primary-color);"),
        Form(
            Label("First Name"),
            Input(name="firstname", type="text", value=user.userdetail.firstname),
            Label("Last Name"),
            Input(name="lastname", type="text", value=user.userdetail.lastname),
            Label("Birthday"),
            Input(name="birthday", type="date", value=user.userdetail.birthday),
            Label("Phone Number"),
            Input(name="phone_number", type="text", value=user.userdetail.phone_number),
            Label("Address"),
            Input(name="address", type="text", value=user.userdetail.address),
            Label("Nationality"),
            Select(
                Option("Thai", selected=user.userdetail.nationality == "Thai"),
                Option("American", selected=user.userdetail.nationality == "American"),
                Option("Other", selected=user.userdetail.nationality == "Other"),
                name="nationality"
            ),
            Label("Gender"),
            Select(
                Option("Male", selected=user.userdetail.gender == "Male"),
                Option("Female", selected=user.userdetail.gender == "Female"),
                Option("Prefer not to tell", selected=user.userdetail.gender == "Prefer not to tell"),
                name="gender"
            ),
            Button("Save Changes", type="submit", hx_post="/edit-profile", hx_target="#profile-card", hx_swap="outerHTML"),
            method="post",
            style="display: flex; flex-direction: column; gap: 10px;"
        ),
        id="profile-card",
        style="border: 2px solid var(--primary-color); border-radius: 10px; padding: 20px; margin: 10px;"
    )
@rt("/password")
def get():
    return Container(
        COMMON_STYLES,
        Div(
            H2("Change Your Password", cls="title"),
            Form(
                Div(
                    Label("Current Password", cls="form-label"),
                    Input(name="old_password", type="password", cls="form-input", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("New Password", cls="form-label"),
                    Input(name="new_password", type="password", cls="form-input", required=True,
                          hx_post="/check-password",  # ✅ Sends input to /check-password
                          hx_trigger="input",  # ✅ Fires on input change
                          hx_target="#password-message"),  # ✅ Updates #password-message
                    Div(id="password-message", style="color: red; font-size: 0.9em;"),  # ✅ Error will appear here
                    cls="form-group"
                ),
                Div(
                    Label("Confirm New Password", cls="form-label"),
                    Input(name="confirm_new_password", type="password", cls="form-input", required=True,
                          hx_post="/check-confirm-password",  # ✅ Sends input to /check-confirm-password
                          hx_trigger="input",
                          hx_target="#confirm-password-message",  # ✅ Updates #confirm-password-message
                          hx_include="[name='new_password']"),  # ✅ Includes new_password field in the request
                    Div(id="confirm-password-message", style="color: red; font-size: 0.9em;"),  # ✅ Error will appear here
                    cls="form-group"
                ),
                Button("Change Password", type="submit", cls="btn btn-primary"),
                action="/passwordCheck",
                method="post",
                cls="form-container"
            ),
            Form(
                Button("Back to Home", type="submit", cls="btn btn-secondary", formaction="/home"),
                style="text-align: center; margin-top: 1rem;"
            )
        )
    )
    
    
@rt("/check-confirm-password")
def post(new_password: str = "", confirm_new_password: str = ""):
    print(f"HTMX Confirm Request: {new_password} vs {confirm_new_password}")  # ✅ Debugging log

    if not confirm_new_password:
        return "Please confirm your password."
    if new_password != confirm_new_password:
        return "Passwords do not match."
    
    return "✅ Passwords match!"  # ✅ Returns a success message if valid


@rt("/check-password")
def post(password: str = ""):
    print(f"HTMX Request Received: {password}")  # ✅ Debugging log (check console output)

    if not password:
        return "Please enter a password."
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\"_:{}|<>]", password):
        return "Password must contain at least one special character (!@#$%^&* etc.)."

    return "✅ Password is valid!"  # ✅ Returns a success message if valid

@rt("/passwordCheck", methods=["POST"])
def password_change(old_password: str, new_password: str, confirm_new_password: str):
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    result = user.change_password(old_password, new_password, confirm_new_password)

    if "successfully" in result:
        controller.logout()
        return Container(
            H3(result, style="color: green; text-align: center;"),
            Form(Button("Go Back to Login Page", type="submit", formaction="/logout"))
        )

    return Container(
        H3(result, style="color: red; text-align: center;"),
        Form(Button("Try Again", type="submit", formaction="/password"))
    )

# Logout
@rt("/logout")
def get():
    controller.logout()
    return RedirectResponse('/login', status_code=303)