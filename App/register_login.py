from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
register_login_app = app 

@rt("/register")
def get():
    register_styles = Style("""
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
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .overlay {
            background-color: rgba(0, 0, 0, 0.5);
            min-height: 100vh;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .register-container {
            width: 90%;
            max-width: 450px;
            padding: 40px;
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .register-title {
            text-align: center;
            color: #fff;
            margin-bottom: 30px;
            font-size: 28px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-control {
            width: 100%;
            padding: 12px 15px;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: #fff;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .form-control::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .form-control:focus {
            outline: none;
            background-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(79, 195, 247, 0.5);
            box-shadow: 0 0 0 2px rgba(79, 195, 247, 0.3);
        }
        
        .error-message {
            color: #ff6b6b;
            font-size: 0.9em;
            margin-top: 5px;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        .register-btn {
            width: 100%;
            padding: 12px;
            background-color: rgba(33, 150, 243, 0.8);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
        }
        
        .register-btn:hover {
            background-color: rgba(33, 150, 243, 1);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
        }
        
        .login-link {
            text-align: center;
            margin-top: 20px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .login-link a {
            color: #4fc3f7;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .login-link a:hover {
            color: #81d4fa;
            text-decoration: underline;
        }
    """)

    return Div(
        register_styles,
        Div(
            Div(
                Div(
                    H1("Create Account", cls="register-title"),
                    Form(
                        Div(
                            Input(id="email", name="email", placeholder="Email", type="email", required=True, cls="form-control"),
                            cls="form-group"
                        ),
                        Div(
                            Input(id="password", name="password", placeholder="Password", type="password", required=True,
                                    hx_post="/check-password", hx_trigger="input", hx_target="#password-message", cls="form-control"),
                            Div(id="password-message", cls="error-message"),
                            cls="form-group"
                        ),
                        Div(
                            Input(id="confirm-password", name="confirm_password", placeholder="Confirm Password", type="password", required=True,
                                hx_post="/check-confirm-password", hx_trigger="input", hx_target="#confirm-password-message", cls="form-control"),
                            Div(id="confirm-password-message", cls="error-message"),
                            cls="form-group"
                        ),
                        Div(
                            Input(id="firstname", name="firstname", placeholder="First Name", required=True, cls="form-control"),
                            cls="form-group"
                        ),
                        Div(
                            Input(id="lastname", name="lastname", placeholder="Last Name", required=True, cls="form-control"),
                            cls="form-group"
                        ),
                        Button("Register", cls="register-btn"),
        action="/register",
        method="post"
                    ),
                    P(Span("Already have an account? ", cls=""), A("Login here", href="/login"), cls="login-link"),
                    cls="register-container"
                ),
                cls="overlay"
            )
        )
    )

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
    error_message = None
    
    if len(password) < 6:
        error_message = "Password must be at least 6 characters long."
    elif not re.search(r"[A-Z]", password):
        error_message = "Password must contain at least one uppercase letter."
    elif not re.search(r"[a-z]", password):
        error_message = "Password must contain at least one lowercase letter."
    elif not re.search(r"\d", password):
        error_message = "Password must contain at least one number."
    elif not re.search(r"[!@#$%^&*(),.?\"_:{}|<>]", password):
        error_message = "Password must contain at least one special character (!@#$%^&* etc.)."
    elif password != confirm_password:
        error_message = "Passwords do not match."
        
    if error_message:
        error_styles = Style("""
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
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .overlay {
                background-color: rgba(0, 0, 0, 0.5);
                min-height: 100vh;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .error-container {
                width: 90%;
                max-width: 400px;
                padding: 40px;
                background-color: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
            }
            
            .error-icon {
                font-size: 50px;
                color: #ff6b6b;
                margin-bottom: 20px;
            }
            
            .error-title {
                color: #fff;
                font-size: 24px;
                margin-bottom: 15px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .error-message {
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 30px;
                font-size: 16px;
                line-height: 1.5;
            }
            
            .return-btn {
                padding: 12px 25px;
                background-color: rgba(33, 150, 243, 0.8);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
                width: 100%;
            }
            
            .return-btn:hover {
                background-color: rgba(33, 150, 243, 1);
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
            }
        """)
        
        return Div(
            error_styles,
            Div(
                Div(
                    Div("✕", cls="error-icon"),
                    H2("Registration Failed", cls="error-title"),
                    P(error_message, cls="error-message"),
                    Form(
                        Button("Try Again", cls="return-btn"),
                        action="/register",
                        method="get"
                    ),
                    cls="error-container"
                ),
                cls="overlay"
            )
        )
    else:
        message = controller.register(email, password, firstname, lastname)

    if "successful" in message:
            success_styles = Style("""
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
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                .overlay {
                    background-color: rgba(0, 0, 0, 0.5);
                    min-height: 100vh;
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                .success-container {
                    width: 90%;
                    max-width: 400px;
                    padding: 40px;
                    background-color: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    text-align: center;
                }
                
                .success-icon {
                    font-size: 50px;
                    color: #4CAF50;
                    margin-bottom: 20px;
                }
                
                .success-title {
                    color: #fff;
                    font-size: 24px;
                    margin-bottom: 15px;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                }
                
                .success-message {
                    color: rgba(255, 255, 255, 0.9);
                    margin-bottom: 30px;
                    font-size: 16px;
                    line-height: 1.5;
                }
                
                .login-btn {
                    padding: 12px 25px;
                    background-color: rgba(33, 150, 243, 0.8);
                    color: white;
                    border: none; 
                    border-radius: 8px; 
                    font-size: 16px; 
                    font-weight: 500;
                    cursor: pointer; 
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
                    width: 100%;
                    text-decoration: none;
                    display: inline-block;
                }
                
                .login-btn:hover {
                    background-color: rgba(33, 150, 243, 1);
                    transform: translateY(-3px);
                    box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
                }
            """)
            
            return Div(
                success_styles,
                Div(
                    Div(
                        Div("✓", cls="success-icon"),
                        H2("Registration Successful!", cls="success-title"),
                        P(message, cls="success-message"),
                        A("Go to Login", href="/login", cls="login-btn"),
                        cls="success-container"
                    ),
                    cls="overlay"
            )
        )
    else:
            error_styles = Style("""
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
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                .overlay {
                    background-color: rgba(0, 0, 0, 0.5);
                    min-height: 100vh;
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                
                .error-container {
                    width: 90%;
                    max-width: 400px;
                    padding: 40px;
                    background-color: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    text-align: center;
                }
                
                .error-icon {
                    font-size: 50px;
                    color: #ff6b6b;
                    margin-bottom: 20px;
                }
                
                .error-title {
                    color: #fff;
                    font-size: 24px;
                    margin-bottom: 15px;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                }
                
                .error-message {
                    color: rgba(255, 255, 255, 0.9);
                    margin-bottom: 30px;
                    font-size: 16px;
                    line-height: 1.5;
                }
                
                .return-btn {
                    padding: 12px 25px;
                    background-color: rgba(33, 150, 243, 0.8);
                    color: white;
                        border: none; 
                        border-radius: 8px; 
                        font-size: 16px; 
                    font-weight: 500;
                        cursor: pointer; 
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
                    width: 100%;
                }
                
                .return-btn:hover {
                    background-color: rgba(33, 150, 243, 1);
                    transform: translateY(-3px);
                    box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
                }
            """)
            
            return Div(
                error_styles,
                Div(
                    Div(
                        Div("✕", cls="error-icon"),
                        H2("Registration Failed", cls="error-title"),
                        P(message, cls="error-message"),
                        Form(
                            Button("Try Again", cls="return-btn"),
                            action="/register",
                            method="get"
                        ),
                        cls="error-container"
                    ),
                    cls="overlay"
            )
        )

# Login Page
@rt("/login")
def get():
    login_styles = Style("""
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
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .overlay {
            background-color: rgba(0, 0, 0, 0.5);
            min-height: 100vh;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .login-container {
            width: 90%;
            max-width: 400px;
            padding: 40px;
            background-color: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .login-title {
            text-align: center;
            color: #fff;
            margin-bottom: 30px;
            font-size: 28px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .form-group {
            margin-bottom: 20px;
        }
        
        .form-control {
            width: 100%;
            padding: 12px 15px;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: #fff;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .form-control::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .form-control:focus {
            outline: none;
            background-color: rgba(255, 255, 255, 0.2);
            border-color: rgba(79, 195, 247, 0.5);
            box-shadow: 0 0 0 2px rgba(79, 195, 247, 0.3);
        }
        
        .login-btn {
            width: 100%;
            padding: 12px;
            background-color: rgba(33, 150, 243, 0.8);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
        }
        
        .login-btn:hover {
            background-color: rgba(33, 150, 243, 1);
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
        }
        
        .register-link {
            text-align: center;
            margin-top: 20px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .register-link a {
            color: #4fc3f7;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .register-link a:hover {
            color: #81d4fa;
            text-decoration: underline;
        }
        
        .error-message {
            background-color: rgba(255, 107, 107, 0.2);
            border-left: 4px solid #ff6b6b;
            padding: 10px 15px;
            margin-bottom: 20px;
            border-radius: 4px;
            color: #fff;
            font-size: 14px;
            display: none;
        }
    """)

    return Div(
        login_styles,
        Div(
            Div(
                H1("Welcome Back", cls="login-title"),
                Div(id="login-error", cls="error-message"),
        Form(
                    Div(
                        Input(id="email", name="email", placeholder="Email", type="email", required=True, cls="form-control"),
                        cls="form-group"
                    ),
                    Div(
                        Input(id="password", name="password", placeholder="Password", type="password", required=True, cls="form-control"),
                        cls="form-group"
                    ),
                    Button("Login", cls="login-btn"),
                    action="/login",
                    method="post"
                ),
                P(Span("Don't have an account? ", cls=""), A("Register here", href="/register"), cls="register-link"),
                cls="login-container"
            ),
            cls="overlay"
        )
    )

@rt("/login")
def post(email: str, password: str):
    message = controller.login(email, password)
    if "success" in message:
        return RedirectResponse('/home', status_code=303)
    else:
        error_styles = Style("""
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
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .overlay {
                background-color: rgba(0, 0, 0, 0.5);
                min-height: 100vh;
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            .error-container {
                width: 90%;
                max-width: 400px;
                padding: 40px;
                background-color: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.2);
                text-align: center;
            }
            
            .error-icon {
                font-size: 50px;
                color: #ff6b6b;
                margin-bottom: 20px;
            }
            
            .error-title {
                color: #fff;
                font-size: 24px;
                margin-bottom: 15px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            .error-message {
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 30px;
                font-size: 16px;
                line-height: 1.5;
            }
            
            .return-btn {
                padding: 12px 25px;
                background-color: rgba(33, 150, 243, 0.8);
                color: white;
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
                font-weight: 500;
            cursor: pointer; 
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4);
                width: 100%;
            }
            
            .return-btn:hover {
                background-color: rgba(33, 150, 243, 1);
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6);
            }
        """)
        
        return Div(
            error_styles,
            Div(
                Div(
                    Div("✕", cls="error-icon"),
                    H2("Login Failed", cls="error-title"),
                    P(message, cls="error-message"),
                    Form(
                        Button("Return to Login", cls="return-btn"),
                        action="/login",
                        method="get"
                    ),
                    cls="error-container"
                ),
                cls="overlay"
            )
    )
