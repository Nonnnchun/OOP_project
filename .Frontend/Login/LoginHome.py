from fasthtml.common import *
from LoginHomeBack import *
import re

app, rt = fast_app()

# Add this at the top of the file, after the imports
COMMON_STYLES = Style("""
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    :root {
        --primary-color: #FCDE22;
        --secondary-color: #F4D9C1;
        --dark-bg: #1a1f2c;
        --text-light: #E1EBF8;
        --accent-color: #D3ECDC;
        --error-color: #ff6b6b;
        --success-color: #51cf66;
    }

    body {
        margin: 0;
        padding: 0;
        min-height: 100vh;
        background: linear-gradient(135deg, var(--dark-bg), #2d3748, var(--dark-bg));
        font-family: 'Poppins', sans-serif;
        color: var(--text-light);
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .form-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        max-width: 500px;
        margin: 2rem auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-label {
        display: block;
        color: var(--text-light);
        margin-bottom: 0.5rem;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .form-input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-light);
        transition: all 0.3s ease;
        font-size: 1rem;
        font-family: 'Poppins', sans-serif;
    }

    .form-input:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(252, 222, 34, 0.2);
        background: rgba(255, 255, 255, 0.1);
    }

    .btn {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Poppins', sans-serif;
    }

    .btn-primary {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: var(--dark-bg);
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(252, 222, 34, 0.3);
    }

    .btn-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-light);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    .title {
        color: var(--primary-color);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .error-message {
        color: var(--error-color);
        background: rgba(255, 107, 107, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }

    .success-message {
        color: var(--success-color);
        background: rgba(81, 207, 102, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
""")

# ================================
#           ROUTES
# ================================

# Welcome Page
@rt('/')
def home():
    # Modern UI Styles with Anime Theme
    styles = Style("""
        html {
            scroll-behavior: smooth;
        }
        
        body { 
            margin: 0;
            padding: 0;
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1a1f2c, #2d3748, #1a1f2c);
            color: #E1EBF8;
            overflow-x: hidden;
        }

        .background-wrapper {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            z-index: 1;
        }

        .background-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.6;
            filter: brightness(0.7);
        }

        .main-content {
            position: relative;
            z-index: 2;
        }

        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(26, 31, 44, 0.8);
            backdrop-filter: blur(10px);
            z-index: 1000;
            border-bottom: 1px solid rgba(211, 236, 220, 0.1);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.5rem;
            font-weight: bold;
            color: #FDDFD6;
        }

        .traffic-lights {
            display: flex;
            gap: 8px;
        }

        .light {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }

        .red { background-color: #FDDFD6; }
        .yellow { background-color: #FCF9DA; }
        .green { background-color: #D3ECDC; }

        .nav-buttons {
            display: flex;
            gap: 20px;
        }

        .nav-button {
            padding: 8px 20px;
            border: none; 
            border-radius: 5px;
            background: #D8F1F1;
            color: #2D3748;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }

        .nav-button:hover {
            background: #FCDE22;
            transform: translateY(-2px);
        }

        .hero-section {
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        .content-overlay {
            text-align: center;
            padding: 3rem;
            background: rgba(26, 31, 44, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            max-width: 600px;
            margin: 0 20px;
            border: 1px solid rgba(211, 236, 220, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        .info-section {
            background: rgba(26, 31, 44, 0.95);
            padding: 4rem 2rem;
            position: relative;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .info-card {
            background: rgba(225, 235, 248, 0.05);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid rgba(211, 236, 220, 0.1);
            transition: all 0.3s ease;
        }

        .info-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            border-color: rgba(252, 222, 34, 0.2);
        }

        .info-title {
            font-size: 1.5rem;
            color: #FCDE22;
            margin-bottom: 1rem;
            font-weight: bold; 
        }

        .info-text {
            color: #EFF5EE;
            line-height: 1.6;
            opacity: 0.8;
        }

        .footer {
            background: rgba(26, 31, 44, 0.98);
            padding: 3rem 2rem;
            position: relative;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }

        .footer-column {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .footer-title {
            color: #FCDE22;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }

        .footer-link {
            color: #EFF5EE;
            text-decoration: none;
            opacity: 0.7;
            transition: all 0.3s ease;
        }

        .footer-link:hover {
            opacity: 1;
            color: #FCDE22;
        }

        .copyright {
            text-align: center;
            color: #EFF5EE;
            opacity: 0.6;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(211, 236, 220, 0.1);
        }

        /* Scroll indicator */
        .scroll-indicator {
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            color: #EFF5EE;
            opacity: 0.7;
            animation: bounce 2s infinite;
            cursor: pointer; 
            z-index: 10;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0) translateX(-50%); }
            50% { transform: translateY(-10px) translateX(-50%); }
        }

        .welcome-text {
            font-size: 2.8rem;
            margin-bottom: 1.5rem;
            color: #2D3748;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            font-weight: bold;
            background: linear-gradient(135deg, #2D3748, #4A5568);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .description {
            font-size: 1.2rem;
            margin-bottom: 2.5rem;
            color: #4A5568;
            line-height: 1.8;
            font-weight: 500;
        }

        .cta-button {
            padding: 15px 50px;
            font-size: 1.2rem;
            background: linear-gradient(135deg, #FCDE22, #F4D9C1);
            color: #2D3748;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(252, 222, 34, 0.3);
        }

        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(252, 222, 34, 0.4);
            background: linear-gradient(135deg, #F4D9C1, #FCDE22);
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        .floating {
            animation: float 4s ease-in-out infinite;
        }

        /* Additional decorative elements */
        .content-overlay::before {
            content: '';
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            border-radius: 25px;
            background: linear-gradient(135deg, #D3ECDC, #FCF9DA);
            z-index: -1;
            opacity: 0.5;
        }
    """)

    # Header with Traffic Lights and Navigation
    header = Div(
        Div(
            Div(cls="light red"),
            Div(cls="light yellow"),
            Div(cls="light green"),
            cls="traffic-lights"
        ),
        Div("Shit Airlines", cls="logo"),
        Div(
            Form(Button("Login", cls="nav-button", formaction="/login")),
            Form(Button("Register", cls="nav-button", formaction="/register")),
            cls="nav-buttons"
        ),
        cls="header"
    )

    # Main Content Structure
    main_content = Div(
        # Background wrapper
        Div(
            Img(src="/Picture/fu7.jpg", cls="background-image"),
            cls="background-wrapper"
        ),
        
        # Content
        Div(
            # Hero Section
            Div(
                Div(
                    H1("Welcome to Shit Airlines", cls="welcome-text floating"),
                    P("""Embark on a journey of comfort and elegance. 
                    Where every flight becomes an unforgettable experience.""", 
                    cls="description"),
                    Form(
                        Button("Start Your Journey", 
                            cls="cta-button",
                            formaction="/login"
                        )
                    ),
                    cls="content-overlay"
                ),
                # Scroll indicator with smooth scroll to about section
                A("↓ Scroll to explore", href="#about", cls="scroll-indicator"),
                cls="hero-section"
            ),

            # Information Section
            Div(
                Div(
                    # About Us
                    Div(
                        H3("About Us", cls="info-title"),
                        P("""Shit Airlines is your premier choice for comfortable and reliable air travel. 
                        We pride ourselves on exceptional service and unforgettable experiences.""",
                        cls="info-text"),
                        cls="info-card"
                    ),
                    # Our Services
                    Div(
                        H3("Our Services", cls="info-title"),
                        P("""From economy to first class, we offer a range of services tailored to your needs. 
                        Enjoy comfortable seating, delicious meals, and entertainment.""",
                        cls="info-text"),
                        cls="info-card"
                    ),
                    # Why Choose Us
                    Div(
                        H3("Why Choose Us", cls="info-title"),
                        P("""Experience unmatched comfort, competitive prices, and a dedication to safety. 
                        Join thousands of satisfied travelers who choose Shit Airlines.""",
                        cls="info-text"),
                        cls="info-card"
                    ),
                    cls="info-grid"
                ),
                cls="info-section",
                id="about"
            ),

            # Footer
            Div(
                Div(
                    # Company Info
                    Div(
                        H4("THE COMPANY", cls="footer-title"),
                        A("ABOUT CGS", href="#about", cls="footer-link"),
                        cls="footer-column"
                    ),
                    # Customer Service
                    Div(
                        H4("CUSTOMER SERVICE", cls="footer-title"),
                        A("CONTACT US", href="#contact", cls="footer-link"),
                        A("STORE LOCATOR", href="#stores", cls="footer-link"),
                        A("DELIVERY INFORMATION", href="#delivery", cls="footer-link"),
                        A("PAYMENTS", href="#payments", cls="footer-link"),
                        A("RETURN & REFUNDS", href="#returns", cls="footer-link"),
                        A("PRODUCT CARE", href="#care", cls="footer-link"),
                        A("SIZE GUIDE", href="#size-guide", cls="footer-link"),
                        A("FAQ", href="#faq", cls="footer-link"),
                        cls="footer-column"
                    ),
                    # Legal
                    Div(
                        H4("LEGAL", cls="footer-title"),
                        A("PRIVACY POLICY", href="#privacy", cls="footer-link"),
                        A("TERMS & CONDITIONS", href="#terms", cls="footer-link"),
                        A("COOKIE SETTINGS", href="#cookies", cls="footer-link"),
                        cls="footer-column"
                    ),
                    # Follow Us
                    Div(
                        H4("FOLLOW US", cls="footer-title"),
                        A("FACEBOOK", href="https://www.facebook.com/", cls="footer-link", target="_blank"),
                        A("LINE OFFICIAL", href="https://line.me/", cls="footer-link", target="_blank"),
                        A("INSTAGRAM", href="https://www.instagram.com/", cls="footer-link", target="_blank"),
                        A("PINTEREST", href="https://www.pinterest.com/", cls="footer-link", target="_blank"),
                        A("TIKTOK", href="https://www.tiktok.com/", cls="footer-link", target="_blank"),
                        A("SPOTIFY", href="https://www.spotify.com/", cls="footer-link", target="_blank"),
                        cls="footer-column"
                    ),
                    cls="footer-content"
                ),
                Div(
                    "©2025 Shit Airlines Public Company Limited. All Right Reserved.",
                    cls="copyright"
                ),
                cls="footer",
                id="footer"
            ),
            cls="main-content"
        )
    )

    return Title("Shit Airlines 🌟🛩️"), styles, header, main_content

# Registration Page
@rt("/register")
def get():
    form = Form(
        Input(id="email", name="email", placeholder="Email", type="email"),
        Input(id="password", name="password", placeholder="Password", type="password", 
            hx_post="/check-password", hx_trigger="input", hx_target="#password-message"),
        Div(id="password-message", style="color: red; font-size: 0.9em;"),
        Input(id="firstname", name="firstname", placeholder="First Name"),
        Input(id="lastname", name="lastname", placeholder="Last Name"),
        Button("Register"),
        action="/register", method="post"
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

@rt("/register")
def post(email: str, password: str, firstname: str, lastname: str):
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

# Home Page (Only Accessible if Logged In)
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
                    Form(Button("View", type="submit", cls="btn btn-primary", formaction="/booking")),
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

@rt("/flight_search")
def search():
    airport_options = [
        Option(f"{airport.name} ({airport.code})", value=airport.code)
        for airport in [jfk, lax, sfo, bkk, cnx]
    ]

    return Container(
        COMMON_STYLES,
        Div(
            H1("Find a Flight", cls="title"),
            Form(
                Div(
                    Label("From", cls="form-label"),
                    Select(*airport_options, name="origin", required=True, cls="form-input"),
                    cls="form-group"
                ),
                Div(
                    Label("To", cls="form-label"),
                    Select(*airport_options, name="destination", required=True, cls="form-input"),
                    cls="form-group"
                ),
                Div(
                    Label("Date", cls="form-label"),
                    Input(type="date", name="date", required=True, cls="form-input"),
                    cls="form-group"
                ),
                Button("Search Flights", type="submit", cls="btn btn-primary"),
                action="/search_results",
                method="post",
                cls="form-container"
            ),
            Form(
                Button("Back to Home", type="submit", cls="btn btn-secondary", formaction="/home"),
                style="text-align: center; margin-top: 1rem;"
            )
        )
    )

@rt("/search_results", methods=["POST"])
async def search_results(request):
    form_data = await request.form()

    origin_code = form_data.get("origin", "").strip()
    destination_code = form_data.get("destination", "").strip()
    date = form_data.get("date", "").strip()

    try:
        search_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return Div("Invalid date format!", cls="error")

    matching_flights = [
        flight for flight in controller.flights
        if flight.origin == origin_code
        and flight.destination == destination_code
        and datetime.strptime(flight.departure_time, "%Y-%m-%d %H:%M") >= search_date
    ]

    if not matching_flights:
        return Title("Search Results"), Div(
            Div("No flights found!", cls="results-container"),
            Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")
        )


    flight_cards = [
        Div(
            H3(f"{flight.origin} ✈ {flight.destination}", style="color: var(--primary-color);"),
            P(f"Departure: {flight.departure_time}"),
            P(f"Arrival: {flight.arrive_time}"),
            P(f"Aircraft: {flight.plane.aircraft}"),
            Form(
                Hidden(name="flight_id", value=flight.flight_id),  # ✅ Store flight ID
                Button("Book This Flight", type="submit", cls="book-btn", formaction="/seat_map")  # ✅ Now goes to /seat_map
            ),
            cls="flight-card"
        )
        for flight in matching_flights
    ]

    return Title("Search Results"), Div(*flight_cards, cls="results-container"), Form(Button("Back", type="submit", cls="back-btn"), action="/flight_search")



@rt("/seat_map", methods=["GET", "POST"])
async def seat_map(request):

    max_seat_count = 5

    form_data = await request.form() if request.method == "POST" else request.query_params

    flight_id = form_data.get("flight_id", "").strip()
    flight = controller.get_flight_by_id(flight_id)

    if not flight:
        return Title("Error"), H1("Flight not found")

    styles = Style("""
        body { font-family: Arial, sans-serif; background-color: #000000; color: #333; }
        .container { background: white; padding: 20px; border-radius: 10px; 
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); max-width: 800px; margin: 0 auto; }
        .seat-map { display: flex; flex-direction: column; gap: 5px; margin: 20px 0; }
        .row { display: flex; justify-content: center; gap: 5px; margin-bottom: 5px; }
        .seat { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;
                border-radius: 5px; font-size: 12px; position: relative; }
        .seat-checkbox { position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
        .seat-checkbox:checked + .seat-label { border: 2px solid #FF0000; }
        .seat-label { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
        
        /* Seat classes */
        .economy { background-color: #A0D6B4; } /* Light green for economy */
        .business { background-color: #8BB5FE; } /* Light blue for business */
        .first-class { background-color: #F3B5C1; } /* Light pink for first class */
        
        /* Seat availability */
        .available { border: 1px solid #888; cursor: pointer; }
        .booked { background-color: #ddd; color: #999; cursor: not-allowed; }
        
        /* Legend */
        .legend { display: flex; justify-content: center; gap: 15px; margin-bottom: 20px; }
        .legend-item { display: flex; align-items: center; gap: 5px; font-size: 12px; }
        .legend-color { width: 15px; height: 15px; border-radius: 3px; }
        
        /* Submit button */
        .submit-btn { background-color: #FFEB99; padding: 10px; font-size: 16px;
                    border: 2px solid #F9D01C; border-radius: 8px; font-weight: bold;
                    cursor: pointer; transition: 0.3s ease; margin-top: 20px; width: 100%; }
        .submit-btn:hover { background-color: #F9D01C; }
        
        /* Counter for selected seats */
        .seat-counter { font-weight: bold; margin: 10px 0; }
    """)

    # ✅ Ensure a booking is created
    if request.method == "GET":
        booking = controller.create_booking(flight_id)
        if not booking:
            return Title("Error"), H1("Could not create booking")
    else:
        booking_ref = form_data.get("booking_ref", "").strip()
        booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
        if not booking:
            return Title("Error"), H1("Booking not found")

    # ✅ Seat Map Logic
    seat_rows = {}
    for seat in flight.plane.seats:
        row_num = ''.join(filter(str.isdigit, seat.seat_id))
        if row_num not in seat_rows:
            seat_rows[row_num] = []
        seat_rows[row_num].append(seat)

    seat_map_html = []
    for row_num in sorted(seat_rows.keys(), key=int):
        seats_in_row = sorted(seat_rows[row_num], key=lambda s: ''.join(filter(str.isalpha, s.seat_id)))
        seat_buttons = []

        for seat in seats_in_row:
            seat_class = "available" if seat.is_available() else "booked"
            seat_type_class = "economy" if seat.seat_type == "Economy" else "business" if seat.seat_type == "Business" else "first-class"

            if seat.is_available():
                seat_buttons.append(
                    Div(
                        Input(type="checkbox", name="seat_ids", value=seat.seat_id, 
                            cls="seat-checkbox", 
                            onclick="checkSeatLimit(this)"),
                        Div(seat.seat_id, cls="seat-label"),
                        cls=f"seat {seat_class} {seat_type_class}"
                    )
                )
            else:
                seat_buttons.append(Div(seat.seat_id, cls=f"seat {seat_class} {seat_type_class}"))

        seat_map_html.append(Div(*seat_buttons, cls="row"))

    legend = Div(
        Div(Div(cls="legend-color economy"), "Economy", cls="legend-item"),
        Div(Div(cls="legend-color business"), "Business", cls="legend-item"),
        Div(Div(cls="legend-color first-class"), "First Class", cls="legend-item"),
        Div(Div(cls="legend-color available"), "Available", cls="legend-item"),
        Div(Div(cls="legend-color booked"), "Booked", cls="legend-item"),
        cls="legend"
    )

    # Javascript to limit seat selection to 5
    seat_limit_script = Script("""
        function checkSeatLimit(checkbox) {
            var checkboxes = document.querySelectorAll('input[name="seat_ids"]:checked');
            var maxSeats = 5; // Change this to dynamically fetch the max seat count
            document.getElementById('selected_seat_count').value = checkboxes.length;
            document.getElementById('selected-count').textContent = checkboxes.length;
            if (checkboxes.length > maxSeats) {
                checkbox.checked = false;
                alert(`You can only select up to ${maxSeats} seats`);
            }
        }
    """)

    return Title("Seat Selection"), styles, seat_limit_script, Div(
        H1(f"Select Seats for Flight {flight_id}"),
        P(f"From {flight.origin} to {flight.destination}"),
        P(f"Departure: {flight.departure_time}"),
        Div("Selected seats: ", Span("0", id="selected-count"), Span(f"/{max_seat_count}", id="max-seat-count"), cls="seat-counter"),
        legend,
        Form(
            Div(*seat_map_html, cls="seat-map"),
            Input(type="hidden", name="booking_ref", value=booking.booking_reference),
            Input(type="hidden", name="selected_seat_count", id="selected_seat_count", value="0"),
            Button("Continue with Selected Seats", type="submit", cls="submit-btn"),
            action="/luggage_calculator",
            method="post",
            cls="container"
        )
    )

@rt("/luggage_calculator", methods=["POST"])
async def luggage_calculator(request):
    # Get form data with await
    form_data = await request.form()

    # Get the selected seat count from the form data
    selected_seat_count = int(form_data.get("selected_seat_count", "1").strip())
    
    # Extract booking reference for passing along
    booking_ref = form_data.get("booking_ref", "").strip()
    
    # Get selected seats for passing along
    seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
    if not isinstance(seat_ids, list):
        seat_ids = [seat_ids]
    
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
        .form-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 400px;
            text-align: center;
        }
        .form-container input {
            width: 100%;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
            background-color: #fff;
        }
        .calculate-btn {
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
            margin-top: 20px;
        }
        .calculate-btn:hover {
            background-color: #F9D01C;
        }
        .person-container {
            border: 1px solid #eee;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .person-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .action-btn {
            background-color: #FFEB99;
            padding: 5px 10px;
            font-size: 14px;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
        }
        .action-btn:hover {
            background-color: #F9D01C;
        }
        .add-person-btn {
            margin-top: 10px;
            background-color: #e6f7ff;
            border: 2px solid #1890ff;
        }
        .add-person-btn:hover {
            background-color: #bae7ff;
        }
        .seat-info {
            margin-bottom: 15px;
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 5px;
            border: 1px solid #d0e8ff;
        }
    """)

    # Add JavaScript for dynamic person management with seat count limitation
    script = Script("""
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize with one person container
        const seatCount = parseInt(document.getElementById('selected_seat_count').value, 10);
        
        // If we have more than one seat, add appropriate number of person containers
        for (let i = 1; i < seatCount; i++) {
            addPerson();
        }
        
        // Update the add person button visibility
        updateAddPersonButtonVisibility();
    });
    
    function addPerson() {
        const personCount = document.querySelectorAll('.person-container').length;
        const maxPersons = parseInt(document.getElementById('selected_seat_count').value, 10);
        
        if (personCount >= maxPersons) {
            alert(`Maximum ${maxPersons} people allowed based on selected seats.`);
            return;
        }

        const personContainer = document.createElement('div');
        personContainer.className = 'person-container';
        personContainer.id = `person-${personCount + 1}`;

        personContainer.innerHTML = `
            <div class="person-header">
                <h3>Person ${personCount + 1}</h3>
                <button type="button" class="action-btn" onclick="removePerson(${personCount + 1})">Remove</button>
            </div>
            <div>
                <label>Luggage Weight (kg):</label>
                <input type="number" name="weight_${personCount + 1}" min="1" max="50" value="20" required>
            </div>
        `;

        const addButton = document.getElementById('add-person-button');
        document.getElementById('people-container').insertBefore(personContainer, addButton);

        document.getElementById('person_count').value = personCount + 1;
        
        // Update add person button visibility
        updateAddPersonButtonVisibility();
    }
    
    function removePerson(personId) {
        const element = document.getElementById(`person-${personId}`);
        element.remove();
        
        // Renumber remaining people
        const personContainers = document.querySelectorAll('.person-container');
        personContainers.forEach((container, index) => {
            container.id = `person-${index + 1}`;
            container.querySelector('h3').textContent = `Person ${index + 1}`;
            container.querySelector('button').setAttribute('onclick', `removePerson(${index + 1})`);
            container.querySelector('input[type="number"]').name = `weight_${index + 1}`;
        });
        
        // Update the person count
        document.getElementById('person_count').value = personContainers.length;
        
        // Update add person button visibility
        updateAddPersonButtonVisibility();
    }
    
    function updateAddPersonButtonVisibility() {
        const personCount = document.querySelectorAll('.person-container').length;
        const maxPersons = parseInt(document.getElementById('selected_seat_count').value, 10);
        const addButton = document.getElementById('add-person-button');
        
        if (personCount >= maxPersons) {
            addButton.style.display = 'none';
        } else {
            addButton.style.display = 'block';
        }
    }
    """)

    # Hidden field to track the number of people (start with 1)
    person_count = Input(type="hidden", name="person_count", value="1", id="person_count")

    submit = Button("Calculate Total Price", type="submit", cls="calculate-btn")

    # Build the full UI
    return Title("Multi-Person Luggage Calculator"), styles, script, Div(
        H1("Calculate Luggage Price"),
        Form(
            # Display information about selected seats
            Div(cls="seat-info", children=[
                H3(f"Selected Seats: {selected_seat_count}"),
                P(f"You can add up to {selected_seat_count} people for luggage calculation.")
            ]),
            
            # Container for all person entries
            Div(
                H3("Luggage Information"),
                # Start with one person
                Div(
                    Div(
                        H3("Person 1"),
                        style="margin-bottom: 10px;"
                    ),
                    Div(Label("Luggage Weight (kg):"), 
                        Input(
                            type="number", 
                            name="weight_1", 
                            min="1", 
                            max="50", 
                            value="20",
                            required=True
                        )
                    ),
                    cls="person-container",
                    id="person-1"
                ),
                # Button to add more people
                Button(
                    "Add Person", 
                    type="button", 
                    onclick="addPerson()",
                    cls="action-btn add-person-btn",
                    id="add-person-button"
                ),
                id="people-container"
            ),
            
            # Hidden input for person count
            person_count,
            
            # Hidden input for the selected seat count
            Input(type="hidden", id="selected_seat_count", name="selected_seat_count", value=str(selected_seat_count)),
            
            # Pass along the booking reference and selected seats
            Input(type="hidden", name="booking_ref", value=booking_ref),
            *[Input(type="hidden", name="seat_ids", value=seat_id) for seat_id in seat_ids],
            
            # Submit button
            submit,
            action="/luggage_results",
            method="post",
            cls="form-container"
        )
    )

@rt("/select_seat", methods=["GET", "POST"])
async def select_seat(request):
    # Debug output for all parameters
    print("DEBUG request method:", request.method)
    
    booking_ref = ""
    seat_id = ""
    
    try:
        if request.method == "GET":
            booking_ref = request.args.get("booking_ref", "")
            seat_id = request.args.get("seat_id", "")
        elif request.method == "POST":
            form_data = await request.form()
            booking_ref = form_data.get("booking_ref", "")
            seat_id = form_data.get("seat_id", "")
        
        # Debug output
        print(f"DEBUG: Retrieved booking_ref={booking_ref}, seat_id={seat_id}")
    except Exception as e:
        print(f"Error processing request parameters: {e}")
        # Fallback to manual URL parsing
        query_string = str(request.url).split('?')[-1] if '?' in str(request.url) else ""
        query_params = {}
        for param in query_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                query_params[key] = value
        booking_ref = query_params.get("booking_ref", "")
        seat_id = query_params.get("seat_id", "")

    
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
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 400px;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
            text-align: left;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .submit-btn {
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
            margin-top: 20px;
        }
        .submit-btn:hover {
            background-color: #F9D01C;
        }
    """)
    
    return Title("Passenger Details"), styles, Div(
        H1("Enter Passenger Details"),
        P(f"Seat Selected: {seat_id}"),
        Form(
            Div(
                Div(
                    Label("Title:"),
                    Select(
                        Option("Mr"),
                        Option("Ms"),
                        Option("Mrs"),
                        Option("Dr"),
                        name="title",
                        required=True
                    ),
                    cls="form-group"
                ),
                Div(
                    Label("First Name:"),
                    Input(type="text", name="firstname", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Last Name:"),
                    Input(type="text", name="lastname", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Email:"),
                    Input(type="email", name="email", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Phone Number:"),
                    Input(type="tel", name="phone", required=True),
                    cls="form-group"
                ),
                Input(type="hidden", name="booking_ref", value=booking_ref),
                Input(type="hidden", name="seat_id", value=seat_id),
                Button("Confirm Selection", type="submit", cls="submit-btn"),
                action="/confirm_seat",
                method="post"
            ),
            cls="container"
        )
    )

@rt("/confirm_seat", methods=["POST"])
async def confirm_seat(request):
    form_data = await request.form()
    
    # Print all form data for debugging
    print("DEBUG confirm_seat form data:", dict(form_data))

    # Extract passenger details
    title = form_data.get("title", "")
    firstname = form_data.get("firstname", "")
    lastname = form_data.get("lastname", "")
    email = form_data.get("email", "")
    phone = form_data.get("phone", "")
    booking_ref = form_data.get("booking_ref", "")
    seat_id = form_data.get("seat_id", "")

    # Debug output
    print(f"DEBUG: Processing booking={booking_ref}, seat={seat_id}")
    
    # Create passenger info dictionary
    passenger_info = {
        'title': title,
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'phone': phone
    }
    
    # Select seat
    success = controller.select_seat(booking_ref, seat_id, passenger_info)
    
    if success:
        # Find the booking to display details
        booking = None
        for b in controller.booking_list:
            if b.booking_reference == booking_ref:
                booking = b
                break
        
        if booking:
            # Calculate the price
            price = controller.calculate_booking_price(booking_ref)
            
            # Get flight details
            flight = booking.flight
            
            return Title("Booking Confirmed"), styles, Div(
                H1("Booking Confirmed!"),
                P(f"Your seat has been successfully booked.", cls="success"),
                Div(
                    Div(
                        Span("Booking Reference: ", cls="detail-label"),
                        Span(booking_ref),
                        cls="detail-row"
                    ),
                    Div(
                        Span("Passenger: ", cls="detail-label"),
                        Span(f"{title} {firstname} {lastname}"),
                        cls="detail-row"
                    ),
                    Div(
                        Span("Flight: ", cls="detail-label"),
                        Span(f"{flight.flight_id}: {flight.origin.code} to {flight.destination.code}"),
                        cls="detail-row"
                    ),
                    Div(
                        Span("Departure: ", cls="detail-label"),
                        Span(flight.departure_time),
                        cls="detail-row"
                    ),
                    Div(
                        Span("Seat: ", cls="detail-label"),
                        Span(seat_id),
                        cls="detail-row"
                    ),
                    Div(
                        Span("Seat Type: ", cls="detail-label"),
                        Span(booking.seat.seat_type),
                        cls="detail-row"
                    ),
                    cls="details"
                ),
                Div(
                    f"Total Price: ${price:.2f}",
                    cls="price"
                ),
                A("Return to Home", href="/", cls="home-btn"),
                cls="container"
            )
        else:
            return Title("Error"), styles, Div(
                H1("Booking Error"),
                P(f"We could not find your booking. Please try again.", cls="error"),
                A("Return to Home", href="/", cls="home-btn"),
                cls="container"
            )
    else:
        return Title("Error"), styles, Div(
            H1("Seat Selection Failed"),
            P(f"We could not book the selected seat. It may have been taken by another passenger.", cls="error"),
            A("Try Again", href="/flight_selection", cls="home-btn"),
            cls="container"
        )

serve()