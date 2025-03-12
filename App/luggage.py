from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
luggage_app = app 

@rt("/luggage_calculator", methods=["GET", "POST"])
async def luggage_calculator(request):
    form_data = await request.form()
    booking_ref = form_data.get("booking_ref", "").strip()
    booking = next((b for b in controller.bookings if b.booking_reference == booking_ref), None)
    if not booking:
        return Title("Error"), H1("Booking not found")

    # Get the selected seat count from the form data
    selected_seat_count = int(form_data.get("selected_seat_count", "1").strip())
    
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
            Input(type="hidden", name="booking_ref", value=booking_ref),
            # Pass along the booking reference and selected seats
            *[Input(type="hidden", name="seat_ids", value=seat_id) for seat_id in seat_ids],
            
            # Submit button
            submit,
            action="/passenger_details",
            method="post",
            cls="form-container"
        )
    )