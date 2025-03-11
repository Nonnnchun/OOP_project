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

    return Container(
        COMMON_STYLES,
        Div(
            H1(f"Welcome, {user.userdetail.firstname} {user.userdetail.lastname}", cls="title"),
            P(f"Total points: {user.userdetail.points}", style="text-align: center; margin-bottom: 2rem;"),
            
            Div(
                Card(
                    H3("Find & Book", style="color: var(--primary-color);"),
                    P("Find a flight"),
                    Form(Button("Search", type="submit", cls="btn btn-primary", formaction="/flight_search")),
                    style="text-align: center;"
                ),
                
                Card(
                    H3("View Profile", style="color: var(--primary-color);"),
                    P("View my personal details"),
                    Form(Button("View", type="submit", cls="btn btn-primary", formaction="/profile")),
                    style="text-align: center;"
                ),
                
                Card(
                    H3("My Bookings", style="color: var(--primary-color);"),
                    P("View all booked flights"),
                    Form(Button("View", type="submit", cls="btn btn-primary", formaction="/manage-booking")),
                    style="text-align: center;"
                ),
                
                Card(
                    H3("Promocode", style="color: var(--primary-color);"),
                    P("View all of my promocodes"),
                    Form(Button("View", type="submit", cls="btn btn-primary", formaction="/promocode")),
                    style="text-align: center;"
                ),
                
                Card(
                    H3("Change Password", style="color: var(--primary-color);"),
                    P("New pass, new security"),
                    Form(Button("Change", type="submit", cls="btn btn-primary", formaction="/password")),
                    style="text-align: center;"
                ),
                cls="grid"
            ),

            Form(
                Button("Logout", type="submit", cls="btn btn-secondary", formaction="/logout"),
                style="text-align: center; margin-top: 2rem;"
            )
        )
    )

@rt("/profile")
def get():
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)

    return Container(
        COMMON_STYLES,
        Div(
            H1("My Profile", cls="title"),
            Div(
                Div(
                    H3("Profile Information", style="color: var(--primary-color); margin-bottom: 1.5rem;"),
                    P(f"Name: {user.userdetail.firstname} {user.userdetail.lastname}"),
                    P(f"Birthday: {user.userdetail.birthday}"),
                    P(f"Gender: {user.userdetail.gender}"),
                    P(f"Nationality: {user.userdetail.nationality}"),
                    P(f"Phone: {user.userdetail.phone_number}"),
                    P(f"Address: {user.userdetail.address}"),
                    Div(
                        Form(
                            Button("Edit", cls="btn btn-primary", formaction="/edit-profile"),
                            style="display: inline-block; margin-right: 1rem;"
                        ),
                        Form(
                            Button("Back", cls="btn btn-secondary", formaction="/home"),
                            style="display: inline-block;"
                        )
                    ),
                    cls="card"
                )
            )
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