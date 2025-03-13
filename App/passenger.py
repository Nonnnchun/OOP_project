from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
passenger_app = app 

@rt("/passenger_details", methods=["GET", "POST"])
async def passenger_details(request):
    if request.method == "POST":
        form_data = await request.form()
        
        booking_ref = form_data.get("booking_ref", "").strip()
        seat_ids = form_data.getlist("seat_ids") if hasattr(form_data, "getlist") else form_data.get("seat_ids", [])
        if not isinstance(seat_ids, list):
            seat_ids = [seat_ids]
        
        booking = controller.search_booking(booking_ref)

        person_count = int(form_data.get("person_count", "1"))
        
        total_weight = booking.calculate_weights(form_data)
        
        booking.add_luggage(Luggage(total_weight))

        luggage_weight_price = booking.luggage.calculate_price()

        seat_info = []
        for seat_id in seat_ids:
            seat_info.append({"id": seat_id,})
        
    styles = Style("""
        /* General Styles */
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #fff;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 800px;
            margin: 20px auto;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(255, 255, 255, 0.1);
        }

        h1, h2, h3 {
            color: #fff;
            text-align: center;
        }

        p {
            color: #bbb;
        }

        /* Form Styles */
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            margin-bottom: 15px;
        }

        label {
            font-weight: bold;
            margin-bottom: 5px;
        }

        input, select, button {
            padding: 10px;
            border: 1px solid #444;
            border-radius: 5px;
            background: #222;
            color: #fff;
        }

        button {
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }

        /* Passenger Section */
        .passenger-section {
            padding: 15px;
            background: #2a2a2a;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .passenger-title {
            color: #007BFF;
        }

        /* Booking Info */
        .booking-info {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }

        /* Action Buttons */
        .action-buttons {
            display: flex;
            justify-content: space-between;
        }

        .back-btn {
            background-color: #6c757d;
        }

        .back-btn:hover {
            background-color: #5a6268;
        }

        .confirm-btn {
            background-color: #28a745;
        }

        .confirm-btn:hover {
            background-color: #218838;
        }

        /* Booking Summary */
        .booking-ref {
            font-size: 18px;
            font-weight: bold;
            color: #007BFF;
            text-align: center;
            margin-bottom: 15px;
        }

        .passenger-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .passenger-item {
            padding: 10px;
            border-radius: 5px;
            background: #2a2a2a;
        }

        /* Price Summary */
        .price-summary {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 5px;
        }

        .price-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }

        .total-price {
            font-weight: bold;
            font-size: 18px;
            color: #28a745;
        }

        /* Payment Page */
        .payment-btn {
            background-color: #dc3545;
        }

        .payment-btn:hover {
            background-color: #c82333;
        }

        .success-icon {
            font-size: 50px;
            color: #28a745;
            text-align: center;
            margin-bottom: 15px;
        }

        /* Flight Details */
        .flight-details {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }

        /* Luggage Details */
        .luggage-details {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }

        /* Validation Styles */
        .error-message {
            color: #dc3545;
            font-size: 12px;
            margin-top: 5px;
        }

        input:invalid {
            border-color: #dc3545;
        }

        .validation-info {
            font-size: 12px;
            color: #6c757d;
            margin-top: 3px;
        }
    """)

    # JavaScript for validation
    validation_script = Script("""
        // Function to calculate age from DOB
        function calculateAge(birthDate) {
            const today = new Date();
            const birth = new Date(birthDate);
            let age = today.getFullYear() - birth.getFullYear();
            const monthDiff = today.getMonth() - birth.getMonth();
            
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
                age--;
            }
            
            return age;
        }

        // Function to validate date of birth
        function validateDOB(input) {
            const dob = input.value;
            const age = calculateAge(dob);
            const errorElement = document.getElementById(input.id + '-error');
            
            if (age < 5) {
                errorElement.textContent = 'Passenger must be at least 5 years old';
                input.setCustomValidity('Passenger must be at least 5 years old');
                return false;
            } else {
                errorElement.textContent = '';
                input.setCustomValidity('');
                return true;
            }
        }

        // Function to validate phone number (10 digits only)
        function validatePhone(input) {
            const phone = input.value;
            const phonePattern = /^[0-9]{10}$/;
            const errorElement = document.getElementById(input.id + '-error');
            
            if (!phonePattern.test(phone)) {
                if (phone.length !== 10) {
                    errorElement.textContent = 'Phone number must be exactly 10 digits';
                } else {
                    errorElement.textContent = 'Phone number must contain only digits';
                }
                input.setCustomValidity('Phone number must be exactly 10 digits');
                return false;
            } else {
                errorElement.textContent = '';
                input.setCustomValidity('');
                return true;
            }
        }

        // Format phone number as user types
        function formatPhoneNumber(input) {
            // Remove any non-digit characters
            let phone = input.value.replace(/\D/g, '');
            
            // Truncate to 10 digits if longer
            if (phone.length > 10) {
                phone = phone.substring(0, 10);
            }
            
            input.value = phone;
            
            // Validate the current value
            validatePhone(input);
            
            // Update character count indicator
            const countElement = document.getElementById(input.id + '-count');
            if (countElement) {
                countElement.textContent = phone.length + '/10';
            }
        }

        // Set max date for DOB fields (must be at least 5 years old)
        function setMaxDate() {
            const dobInputs = document.querySelectorAll('input[type="date"]');
            const today = new Date();
            const maxDate = new Date(today.getFullYear() - 5, today.getMonth(), today.getDate());
            const maxDateStr = maxDate.toISOString().split('T')[0];
            
            dobInputs.forEach(input => {
                input.setAttribute('max', maxDateStr);
            });
        }

        // Validate form before submission
        function validateForm(form) {
            let isValid = true;
            
            // Validate all DOB fields
            const dobInputs = form.querySelectorAll('input[type="date"]');
            dobInputs.forEach(input => {
                if (!validateDOB(input)) {
                    isValid = false;
                }
            });
            
            // Validate all phone fields
            const phoneInputs = form.querySelectorAll('input[type="tel"]');
            phoneInputs.forEach(input => {
                if (!validatePhone(input)) {
                    isValid = false;
                }
            });
            
            return isValid;
        }

        // Initialize validation when page loads
        window.onload = function() {
            setMaxDate();
            
            // Add event listeners to DOB fields
            const dobInputs = document.querySelectorAll('input[type="date"]');
            dobInputs.forEach(input => {
                input.addEventListener('change', function() {
                    validateDOB(this);
                });
            });
            
            // Add event listeners to phone fields
            const phoneInputs = document.querySelectorAll('input[type="tel"]');
            phoneInputs.forEach(input => {
                input.addEventListener('input', function() {
                    formatPhoneNumber(this);
                });
                
                // Initialize count display
                const countElement = document.getElementById(input.id + '-count');
                if (countElement) {
                    countElement.textContent = input.value.length + '/10';
                }
            });
        }
    """)

    passenger_forms = []
    for i, seat in enumerate(seat_info):
        passenger_forms.append(
            Div(
                H3(f"Seat {seat['id']}", cls="passenger-title"),
                Div(
                    Label("First Name", For=f"first_name_{i}"),
                    Span("*", cls="required"),
                    Input(type="text", id=f"first_name_{i}", name=f"first_name_{i}", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Last Name", For=f"last_name_{i}"),
                    Span("*", cls="required"),
                    Input(type="text", id=f"last_name_{i}", name=f"last_name_{i}", required=True),
                    cls="form-group"
                ),
                Div(
                    Label("Date of Birth", For=f"dob_{i}"),
                    Span("*", cls="required"),
                    Input(type="date", id=f"dob_{i}", name=f"dob_{i}", required=True),
                    Div(id=f"dob_{i}-error", cls="error-message"),
                    Div("Passenger must be at least 5 years old", cls="validation-info"),
                    cls="form-group"
                ),
                Div(
                    Label("Phone", For=f"phone_{i}"),
                    Span("*", cls="required"),
                    Input(type="tel", id=f"phone_{i}", name=f"phone_{i}", required=True, 
                          pattern="[0-9]{10}", maxlength="10", minlength="10"),
                    Div(id=f"phone_{i}-error", cls="error-message"),
                    Div(
                        Span("Must be exactly 10 digits", cls="validation-info"),
                        Span(id=f"phone_{i}-count", cls="validation-info", style="float: right;"),
                    ),
                    cls="form-group"
                ),
                cls="passenger-section"
            )
        )
    
    return Title("Passenger Details"), styles, validation_script, Div(
        H1("Passenger Details", cls="header"),
        
        Div(
            H3("Booking Information:"),
            P(Span("Booking Reference: ", cls="booking-ref"), booking_ref),
            P(f"Number of passengers: {person_count}"),
            P("Please enter details for all passengers"),
            cls="booking-info"
        ),
        Form(
            *passenger_forms,
            *[Input(type="hidden", name="seat_ids", value=seat_id) for seat_id in seat_ids],
            Input(type="hidden", name="booking_ref", value=booking_ref),
            Input(type="hidden", name="person_count", value=str(person_count)),
            Input(type="hidden", name="luggage_weight_price", value=luggage_weight_price),
            Div(
                Button("Back to Luggage", type="button", cls="back-btn", onclick="history.back()"),
                Button("Continue to Review", type="submit", cls="confirm-btn"),
                cls="action-buttons"
            ),
            action="/booking_summary",
            method="post",
            onsubmit="return validateForm(this)",
            cls="passenger-form"
        ),
        cls="container"
    )
