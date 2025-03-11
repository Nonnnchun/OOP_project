from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
register_login_app = app 

@rt("/register")
def get():
    form = Form(
        Input(id="email", name="email", placeholder="Email", type="email", required=True),
        Input(id="password", name="password", placeholder="Password", type="password", required=True,
              hx_post="/check-password", hx_trigger="input", hx_target="#password-message"),
        Div(id="password-message", style="color: red; font-size: 0.9em;"),  # Live feedback
        
        Input(id="confirm-password", name="confirm_password", placeholder="Confirm Password", type="password", required=True,
              hx_post="/check-confirm-password", hx_trigger="input", hx_target="#confirm-password-message"),
        Div(id="confirm-password-message", style="color: red; font-size: 0.9em;"),  # Live confirm password check
        
        Input(id="firstname", name="firstname", placeholder="First Name", required=True),
        Input(id="lastname", name="lastname", placeholder="Last Name", required=True),
        Button("Register"),
        action="/register",
        method="post"
    )
    return Titled("Register", form)

@rt("/check-password")
def post(password: str):
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\"_:{}|<>]", password):  # This checks for a special symbol
        return "Password must contain at least one special character (!@#$%^&* etc.)."

    return ""  # No message if password is valid

@rt("/check-confirm-password")
def post(password: str = "", confirm_password: str = ""):
    if confirm_password and password != confirm_password:
        return "Passwords do not match."
    return ""  # No error message if passwords match

@rt("/register")
def post(email: str, password: str, confirm_password: str, firstname: str, lastname: str):
    # Backend password validation (same rules as in /check-password)
    if len(password) < 6:
        return Container(
            P("Password must be at least 6 characters long.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"[A-Z]", password):
        return Container(
            P("Password must contain at least one uppercase letter.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"[a-z]", password):
        return Container(
            P("Password must contain at least one lowercase letter.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"\d", password):
        return Container(
            P("Password must contain at least one number.", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if not re.search(r"[!@#$%^&*(),.?\"_:{}|<>]", password):
        return Container(
            P("Password must contain at least one special character (!@#$%^&* etc.).", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    if password != confirm_password:
        return Container(
            P("Password not match", style="color: red;"),
            Form(Button("Return to Register Page", type="submit", formaction="/register"))
        )
    # If password passes validation, proceed with registration
    message = controller.register(email, password, firstname, lastname)

    if "successful" in message:
        return Container(
            COMMON_STYLES,
            Div(
                H1("Registration Successful!", cls="title"),
                P(message, style="text-align: center; color: var(--success-color); font-size: 1.2rem; margin-bottom: 2rem;"),
                A(
                    "Back to Login",
                    href="/login",
                    style="""display: block;
                    background-color: #FFEB99;
                    color: #333; width: 100%; 
                    padding: 12px; 
                    border: none; 
                    border-radius: 8px; 
                    font-size: 16px; 
                    font-weight: bold; 
                    cursor: pointer; 
                    transition: 0.3s ease; 
                    border: 2px solid #F9D01C;
                    text-decoration: none;
                    text-align: center;
                    max-width: 300px;
                    margin: 0 auto;""",
                    onmouseover="this.style.backgroundColor='#F9D01C'",
                    onmouseout="this.style.backgroundColor='#FFEB99'"
                ),
                cls="card"
            )
        )
    else:
        return Container(
            COMMON_STYLES,
            Div(
                H1("Registration Failed", cls="title"),
                P(message, style="text-align: center; color: var(--error-color); font-size: 1.2rem; margin-bottom: 2rem;"),
                Form(
                    Button("Try Again", 
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
                    formaction="/register",
                    style="max-width: 300px; margin: 0 auto;"
                ),  
                cls="card"
            )
        )

# Login Page
@rt("/login")
def get():
    styles = Style("""
        body {
            margin: 0;
            padding: 0;
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1f2c, #2d3748, #1a1f2c);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-container {
            width: 80%;
            max-width: 1200px;
            height: 600px;
            display: flex;
            background: linear-gradient(135deg, #FDDFD6, #D3ECDC, #FCF9DA);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
            position: relative;
        }

        .login-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(252, 222, 34, 0.1), rgba(244, 217, 193, 0.1));
            pointer-events: none;
            border-radius: 20px;
        }

        .login-image-section {
            flex: 1;
            position: relative;
            overflow: hidden;
        }

        .login-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            opacity: 0.9;
            filter: brightness(0.8);
            transition: transform 0.3s ease;
        }

        .login-image:hover {
            transform: scale(1.05);
        }

        .login-form-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 3rem;
            background: rgba(26, 31, 44, 0.98);
            position: relative;
            z-index: 1;
        }

        .login-header {
            position: absolute;
            top: 2rem;
            left: 2rem;
            right: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .login-logo {
            color: #FCDE22;
            font-size: 1.5rem;
            font-weight: bold;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        .login-logo:hover {
            color: #F4D9C1;
        }

        .register-link {
            color: #FCDE22;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            padding: 0.5rem 1rem;
            border: 1px solid #FCDE22;
            border-radius: 20px;
        }

        .register-link:hover {
            background: #FCDE22;
            color: #1a1f2c;
        }

        .login-form {
            width: 100%;
            max-width: 400px;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(252, 222, 34, 0.2);
            backdrop-filter: blur(10px);
        }

        .form-title {
            color: #FCDE22;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            text-align: center;
            font-weight: bold;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            color: #E1EBF8;
            margin-bottom: 0.5rem;
            font-weight: 500;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid rgba(252, 222, 34, 0.2);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            color: #E1EBF8;
            transition: all 0.3s ease;
            font-size: 1rem;
        }

        .form-input:focus {
            outline: none;
            border-color: #FCDE22;
            box-shadow: 0 0 0 2px rgba(252, 222, 34, 0.2);
            background: rgba(255, 255, 255, 0.1);
        }

        .form-input::placeholder {
            color: rgba(225, 235, 248, 0.5);
        }

        .login-button {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #FCDE22, #F4D9C1);
            border: none;
            border-radius: 8px;
            color: #1a1f2c;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 1rem;
        }

        .login-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(252, 222, 34, 0.3);
            background: linear-gradient(135deg, #F4D9C1, #FCDE22);
        }

        @media (max-width: 768px) {
            .login-container {
                width: 95%;
                flex-direction: column;
                height: auto;
            }

            .login-image-section {
                height: 200px;
            }

            .login-form-section {
                padding: 2rem;
            }
        }
    """)

    return Container(
        Div(
            # Left section with image
            Div(
                Img(src="/Picture/fu4.jpg", cls="login-image"),
                cls="login-image-section"
            ),
            
            # Right section with login form
            Div(
                # Header with logo and register link
                Div(
                    A("Shit Airlines", href="/", cls="login-logo"),
                    A("Register", href="/register", cls="register-link"),
                    cls="login-header"
                ),
                
                # Login Form
        Form(
                    H2("Welcome Back", cls="form-title"),
                    
                    # Email input
                    Div(
                        Label("Email", cls="form-label"),
                        Input(type="email", name="email", placeholder="Enter your email", 
                            required=True, cls="form-input"),
                        cls="form-group"
                    ),
                    
                    # Password input
                    Div(
                        Label("Password", cls="form-label"),
                        Input(type="password", name="password", placeholder="Enter your password", 
                            required=True, cls="form-input"),
                        cls="form-group"
                    ),
                    
                    # Login button
                    Button("Login", type="submit", cls="login-button"),
                    
                    action="/login", method="post",
                    cls="login-form"
                ),
                cls="login-form-section"
            ),
            cls="login-container"
        ),
        styles
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
