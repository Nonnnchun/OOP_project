from fasthtml.common import *
from Backend import *
import re

app, rt = fast_app()
welcome_app = app 


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

