from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
payment_app = app 

@rt("/payment", methods=["POST"])
async def payment(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()
    total_price = float(form_data.get("total_price", "0").strip())
    code = form_data.get("used_code", "").strip().upper()
    code = ''.join(c for c in code if c.isalnum() or c.isdigit())

    styles = Style("""
        body { 
            height: 100vh; 
            margin: 0;
            font-family: 'Arial', sans-serif;
            color: #555;
            text-align: center;
            background-image: url('/Picture/fu7.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            width: 90%;
            max-width: 450px;
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
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .card-details {
            display: flex;
            gap: 10px;
        }
        .card-details > div {
            flex: 1;
        }
        .promocode {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .promocode input {
            flex: 1;
        }
        .payment-btn {
            background-color: #FFEB99;
            color: #333;
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
            margin-top: 20px;
        }
        .payment-btn:hover {
            background-color: #F9D01C;
        }
        .error-message {
            color: #e74c3c;
            font-size: 12px;
            margin-top: 5px;
            display: none;
        }
    """)

    booking = controller.search_booking(booking_ref)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    validation_script = Script("""
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.querySelector('form');
            const cardNumberInput = document.querySelector('input[name="card_number"]');
            const cardNumberError = document.getElementById('card-number-error');
            const expiryInput = document.querySelector('input[name="expiry"]');
            const expiryError = document.getElementById('expiry-error');
            const cvvInput = document.querySelector('input[name="cvv"]');
            const cvvError = document.getElementById('cvv-error');
            const cardTypeSelect = document.querySelector('select[name="card_type"]');
            const totalAmountElement = document.getElementById('total-amount');
            const originalPrice = """ + str(total_price) + """;
            
            // Update total amount when card type changes - simplified to just display original price
            function updateTotalAmount() {
                totalAmountElement.textContent = `Total Amount: ฿${originalPrice.toFixed(2)}`;
                document.getElementById('final-price').value = originalPrice.toFixed(2);
            }
            
            // Initial update
            updateTotalAmount();
            
            // Keep listening for changes on card type (even though it doesn't change the price now)
            cardTypeSelect.addEventListener('change', updateTotalAmount);
            
            // Allow only digits in card number field
            cardNumberInput.addEventListener('input', function(e) {
                this.value = this.value.replace(/\\D/g, '');
                
                // Limit to 16 digits
                if (this.value.length > 16) {
                    this.value = this.value.slice(0, 16);
                }
                
                // Show/hide error message
                if (this.value.length > 0 && this.value.length !== 16) {
                    cardNumberError.style.display = 'block';
                } else {
                    cardNumberError.style.display = 'none';
                }
            });
            
            // Format expiry date (MM/YY)
            expiryInput.addEventListener('input', function(e) {
                this.value = this.value.replace(/\\D/g, '');
                
                if (this.value.length > 2) {
                    this.value = this.value.slice(0, 2) + '/' + this.value.slice(2, 4);
                }
                
                if (this.value.length > 5) {
                    this.value = this.value.slice(0, 5);
                }
                
                if (this.value.length > 0) {
                    const month = parseInt(this.value.slice(0, 2), 10);
                    if (month < 1 || month > 12) {
                        expiryError.style.display = 'block';
                    } else {
                        expiryError.style.display = 'none';
                    }
                } else {
                    expiryError.style.display = 'none';
                }
            });
            
            // Allow only digits in CVV field and limit to 3-4 digits
            cvvInput.addEventListener('input', function(e) {
                this.value = this.value.replace(/\\D/g, '');
                
                if (this.value.length > 4) {
                    this.value = this.value.slice(0, 4);
                }
                
                if (this.value.length > 0 && (this.value.length < 3 || this.value.length > 4)) {
                    cvvError.style.display = 'block';
                } else {
                    cvvError.style.display = 'none';
                }
            });
            
            // Form validation
            form.addEventListener('submit', function(e) {
                let isValid = true;
                
                // Validate card number - must be exactly 16 digits
                if (cardNumberInput.value.length !== 16) {
                    cardNumberError.style.display = 'block';
                    isValid = false;
                }
                
                // Validate expiry date format and value
                const expiryPattern = /^(0[1-9]|1[0-2])\\/([0-9]{2})$/;
                if (!expiryPattern.test(expiryInput.value)) {
                    expiryError.style.display = 'block';
                    isValid = false;
                }
                
                // Validate CVV - must be 3-4 digits
                if (cvvInput.value.length < 3 || cvvInput.value.length > 4) {
                    cvvError.style.display = 'block';
                    isValid = false;
                }
                
                if (!isValid) {
                    e.preventDefault();
                }
            });
        });
    """)
    
    return Title("Payment"), styles, validation_script, Div(
        H1("Payment Details", style="color :#292929;"),
        P(f"Total Amount: ฿{total_price}", id="total-amount"),
        Form(
            Div(
                Label("Card Type:"),
                Select(
                    Option("DebitCard"),
                    Option("CreditCard"),
                    name="card_type",
                    required=True
                ),
                cls="form-group"
            ),
            Div(
                Label("Card Number:"),
                Input(type="text", name="card_number", placeholder="Enter 16 digits", required=True, 
                      pattern="[0-9]{16}", inputmode="numeric", maxlength="16"),
                P("Card number must be exactly 16 digits", id="card-number-error", cls="error-message"),
                cls="form-group"
            ),
            Div(
                Div(
                    Label("Expiry Date:"),
                    Input(type="text", name="expiry", placeholder="MM/YY", required=True, maxlength="5"),
                    P("Enter a valid month/year format (MM/YY)", id="expiry-error", cls="error-message"),
                ),
                Div(
                    Label("CVV:"),
                    Input(type="text", name="cvv", placeholder="XXX", required=True, 
                          pattern="[0-9]{3,4}", inputmode="numeric", maxlength="4"),
                    P("CVV must be 3-4 digits", id="cvv-error", cls="error-message"),
                ),
                cls="card-details form-group"
            ),
            Input(type="hidden", name="booking_ref", value=booking_ref),
            Input(type="hidden", name="final_price", id="final-price", value=str(total_price)),
            Input(type="hidden", name="used_code", value=code),
            Button("Pay Now", type="submit", cls="payment-btn"),
            action="/payment_confirmation",
            method="post",
        ),
        cls="container"
    )
    
@rt("/payment_confirmation", methods=["POST"])
async def payment_confirmation(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()
    code = form_data.get("used_code", "").strip().upper()
    code = ''.join(c for c in code if c.isalnum() or c.isdigit())
    card_type = form_data.get("card_type", "").strip()
    card_number = form_data.get("card_number", "").strip()
    exp = form_data.get("expiry", "").strip()
    cvv = form_data.get("cvv", "").strip()
    final_price = float(form_data.get("final_price", "0").strip())

    user = controller.get_logged_in_user()
    booking = controller.search_booking(booking_ref)
    if not booking:
        return Title("Error"), H1("Booking not found")
    
    if booking.payment.price != final_price:
        booking.payment.price = final_price
    
    user.userdetail.used_code(code)
    booking.update_booking_status()
    user.update_booking_history(booking)
    booking.payment.process_payment(card_type, card_number, cvv, exp)
    
    styles = Style("""
        body { 
            height: 100vh; 
            margin: 0;
            font-family: 'Arial', sans-serif;
            color: #555;
            text-align: center;
            background-image: url('/Picture/fu7.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            width: 90%;
            max-width: 500px;
            text-align: center;
        }
        .success-icon {
            font-size: 60px;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .booking-ref {
            background: rgba(245, 245, 245, 0.8);
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
        }
        .home-btn {
            background-color: #FFEB99;
            color: #333;
            padding: 12px;
            font-size: 16px;
            width: 200px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s ease;
            border: 2px solid #F9D01C;
            margin-top: 20px;
        }
        .home-btn:hover {
            background-color: #F9D01C;
        }
        .details {
            margin-top: 20px;
            text-align: left;
        }
    """)    
    
    return Title("Payment Confirmed"), styles, Div(
        Div("✓", cls="success-icon"),
        H1("Payment Successful!", style="color :#292929;"),
        P("Your flight booking has been confirmed."),
        Div(f"Booking Reference: {booking_ref}", cls="booking-ref"),
        Form(
            Button("Return to Home", type="submit", cls="home-btn"),
            action="/home",
            method="get"
        ),
        cls="container"
    )