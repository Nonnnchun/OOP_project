from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
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
def edit_profile(firstname: str="",lastname: str = "", birthday:str="",phone_number: str = "", address: str = "", gender: str="",nationality: str=""):
    user = controller.get_logged_in_user()
    if not user:
        return RedirectResponse('/login', status_code=303)
    
    if firstname or lastname or phone_number or address or birthday or gender or nationality:  
        user.userdetail.edit_profile(firstname = firstname,lastname=lastname, phone_number=phone_number, address=address, birthday=birthday, gender=gender,nationality= nationality)

        # After saving, show the updated profile card
        return Card(
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

    # Show the edit form
    return Card(
        H3("Edit Profile", style="color: var(--primary-color);"),
        Form(
            Label("Fitst Name"),
            Input(name="firstname", type="text", value=user.userdetail.firstname),
            
            Label("Last Name"),
            Input(name="lastname", type="text", value=user.userdetail.lastname),
            
            Label("Birthday"),
            Input(name="birthday", type="date", value=user.userdetail.birthday),
            
            Label("Phone Number"),
            Input(name="phone_number", type="text", value=user.userdetail.phone_number),
            
            Label("Address"),
            Input(name="address", type="text", value=user.userdetail.address),
            
            Label("National"),
            Select(
                Option("Thai", selected=user.userdetail.nationality == "Thai"),
                Option("American", selected=user.userdetail.nationality == "American"),
                Option("Other", selected=user.userdetail.nationality == "Other"),
                name = "nationality"
            ),
            
            Label("Gender"),
            Select(
                Option("Male", selected=user.userdetail.nationality == "Male"),
                Option("Female", selected=user.userdetail.nationality == "Female"),
                Option("Prefer not to tell", selected=user.userdetail.nationality == "Prefer not to tell"),
                name = "gender"
            ),
            
                
            
            Button("Save Changes", type="submit", 
                hx_post="/edit-profile", 
                hx_target="#profile-card", 
                hx_swap="outerHTML",
                style="background-color: var(--primary-color); padding: 10px; font-size: 16px;"),
            method="post",
            style="display: flex; flex-direction: column; gap: 10px;"
        ),
        id="profile-card",
        style="border: 2px solid var(--primary-color); border-radius: 10px; padding: 20px; margin: 10px;"
    )
    
@rt("/password", methods=["GET", "POST"])
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
                    Input(name="new_password", type="password", cls="form-input", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Confirm New Password", cls="form-label"),
                    Input(name="confirm_new_password", type="password", cls="form-input", required=True),
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