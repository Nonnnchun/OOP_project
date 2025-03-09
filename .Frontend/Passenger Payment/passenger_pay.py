from fasthtml.common import *
from passenger_pay_Back import *

app, rt = fast_app()
    
def themed_card(*children):
    return Container(
        Card(*children), style="max-width: 1050px; margin: 0 auto; padding: 10px;"
    )

@rt('/')
def get():
    return Div(
        Form(
            Label("ผู้โดยสารกี่คน", 
                  Select(*[Option(i, value=i) for i in range(1, 6)], id="passenger_num", name="passenger_num", required=True)
            ),
            Button("ถัดไป", type="submit"), method="post", action="/passenger_details"
        )
    )

@rt('/passenger_details', methods=['POST'])
def passenger_details(passenger_num:int):

    seat_list = []
    for i in range(passenger_num):
        seat_list.append(Seat(i,"Economy"))

    payment = Payment("500")

    booking = Booking(None, None, None, "500", None, seat_list,payment)

    controller.booking_list.append(booking)

    for i in range(passenger_num):
        passenger = PassengerDetail(Adult, seat_list[i])  # Assuming 'Adult' is defined
        booking.passenger_details.append(passenger)

    if passenger_num == 1:
        return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            Form(
                H3("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle1", name="nametitle1", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", name="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", name="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday1", name="day_bday1", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday1", name="month_bday1", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1", name="year_bday1", required=True)
                    ),
                ),
                H4("ข้อมูลติดต่อ"),
                Grid(
                    Label("Email", Input(type="email", id="email1", name="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", name="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                ),
                Button("ถัดไป", type="submit"), method="post", action="/passenger_details_submit1"
            ),
        )
    )
    elif passenger_num == 2:
        return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            Form(
                H3("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle1", name="nametitle1", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", name="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", name="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday1", name="day_bday1", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday1", name="month_bday1", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1", name="year_bday1", required=True)
                    ),
                ),
                H4("ข้อมูลติดต่อ"),
                Grid(
                    Label("Email", Input(type="email", id="email1", name="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", name="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle2", name="nametitle2", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", name="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", name="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday2", name="day_bday2", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday2", name="month_bday2", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2", name="year_bday2", required=True)
                    ),
                ),
                Button("ถัดไป", type="submit"), method="post", action="/passenger_details_submit2"
            ),
        )
    )
    elif passenger_num == 3:
        return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            Form(
                H3("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle1", name="nametitle1", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", name="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", name="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday1", name="day_bday1", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday1", name="month_bday1", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1", name="year_bday1", required=True)
                    ),
                ),
                Grid(
                    Label("Email", Input(type="email", id="email1", name="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", name="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle2", name="nametitle2", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", name="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", name="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday2", name="day_bday2", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday2", name="month_bday2", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2", name="year_bday2", required=True)
                    ),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 3"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle3", name="nametitle3", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name3", name="name3", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname3", name="surname3", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday3", name="day_bday3", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday3", name="month_bday3", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday3", name="year_bday3", required=True)
                    ),
                ),
                Button("ถัดไป", type="submit"), method="post", action="/passenger_details_submit3"
            ),
        )
    )
    elif passenger_num == 4:
        return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            Form(
                H3("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle1", name="nametitle1", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", name="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", name="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday1", name="day_bday1", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday1", name="month_bday1", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1", name="year_bday1", required=True)
                    ),
                ),
                Grid(
                    Label("Email", Input(type="email", id="email1", name="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", name="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle2", name="nametitle2", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", name="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", name="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday2", name="day_bday2", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday2", name="month_bday2", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2", name="year_bday2", required=True)
                    ),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 3"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle3", name="nametitle3", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name3", name="name3", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname3", name="surname3", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday3", name="day_bday3", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday3", name="month_bday3", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday3", name="year_bday3", required=True)
                    ),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 4"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle4", name="nametitle4", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name4", name="name4", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname4", name="surname4", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday4", name="day_bday4", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday4", name="month_bday4", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday4", name="year_bday4", required=True)
                    ),
                ),
                Button("ถัดไป", type="submit"), method="post", action="/passenger_details_submit4"
            ),
        )
    )
    elif passenger_num == 5:
        return Div(
        themed_card(
            H1("✈️ จองเที่ยวบิน AIRXXX"),
            Form(
                H3("ข้อมูลผู้โดยสารหลัก"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle1", name="nametitle1", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name1", name="name1", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname1", name="surname1", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday1", name="day_bday1", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday1", name="month_bday1", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1", name="year_bday1", required=True)
                    ),
                ),
                Grid(
                    Label("Email", Input(type="email", id="email1", name="email1", required=True, placeholder="กรอก E-mail")),
                    Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", name="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 2"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle2", name="nametitle2", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name2", name="name2", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname2", name="surname2", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday2", name="day_bday2", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday2", name="month_bday2", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2", name="year_bday2", required=True)
                    ),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 3"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle3", name="nametitle3", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name3", name="name3", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname3", name="surname3", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday3", name="day_bday3", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday3", name="month_bday3", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday3", name="year_bday3", required=True)
                    ),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 4"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle4", name="nametitle4", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name4", name="name4", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname4", name="surname4", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday4", name="day_bday4", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday4", name="month_bday4", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday4", name="year_bday4", required=True)
                    ),
                ),
                H3("ข้อมูลผู้โดยสารคนที่ 5"),
                Grid(
                    Label("คำนำหน้า",
                          Select(Option("นาย", value="นาย"), Option("นาง", value="นาง"), Option("นางสาว", value="นางสาว"), id="nametitle5", name="nametitle5", required=True)
                    ),
                    Label("ชื่อ", Input(type="text", id="name5", name="name5", required=True, placeholder="กรอกชื่อ")),
                    Label("นามสกุล", Input(type="text", id="surname5", name="surname5", required=True, placeholder="กรอกนามสกุล")),
                ),
                Grid(
                    Label("วันเกิด",
                          Select(*[Option(i, value=i) for i in range(1, 32)], id="day_bday5", name="day_bday5", required=True)
                    ),
                    Label("เดือน",
                          Select(*[Option(i, value=i) for i in range(1, 13)], id="month_bday5", name="month_bday5", required=True)
                    ),
                    Label("ปี",
                          Select(*[Option(i, value=i) for i in range(1900, 2026)], id="year_bday5", name="year_bday5", required=True)
                    ),
                ),
                Button("ถัดไป", type="submit"), method="post", action="/passenger_details_submit5"
            ),
        )
    )

# Handle submission for 1 passenger
@rt('/passenger_details_submit1')
def passenger_details_submit1(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str):
    booking = controller.booking_list[0]
    passenger_details = [
    (nametitle1, name1, surname1, day_bday1, month_bday1, year_bday1, email1, phone_number1)
    ]
    for i, details in enumerate(passenger_details):
        booking.passenger_details[i].update_passenger_details(*details)
    return Redirect('/pay')

# Handle submission for 2 passengers
@rt('/passenger_details_submit2')
def passenger_details_submit2(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str):
    booking = controller.booking_list[0]
    passenger_details = [
    (nametitle1, name1, surname1, day_bday1, month_bday1, year_bday1, email1, phone_number1),
    (nametitle2, name2, surname2, day_bday2, month_bday2, year_bday2, None, None),
    ]
    for i, details in enumerate(passenger_details):
        booking.passenger_details[i].update_passenger_details(*details)
    return Redirect('/pay')

# Handle submission for 3 passengers
@rt('/passenger_details_submit3')
def passenger_details_submit3(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str,
                                nametitle3: str, name3: str, surname3: str, day_bday3: str, month_bday3: str, year_bday3: str):
    booking = controller.booking_list[0]
    passenger_details = [
    (nametitle1, name1, surname1, day_bday1, month_bday1, year_bday1, email1, phone_number1),
    (nametitle2, name2, surname2, day_bday2, month_bday2, year_bday2, None, None),
    (nametitle3, name3, surname3, day_bday3, month_bday3, year_bday3, None, None)
    ]
    for i, details in enumerate(passenger_details):
        booking.passenger_details[i].update_passenger_details(*details)
    return Redirect('/pay')

# Handle submission for 4 passengers
@rt('/passenger_details_submit4')
def passenger_details_submit4(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str,
                                nametitle3: str, name3: str, surname3: str, day_bday3: str, month_bday3: str, year_bday3: str,
                                nametitle4: str, name4: str, surname4: str, day_bday4: str, month_bday4: str, year_bday4: str):
    booking = controller.booking_list[0]
    passenger_details = [
    (nametitle1, name1, surname1, day_bday1, month_bday1, year_bday1, email1, phone_number1),
    (nametitle2, name2, surname2, day_bday2, month_bday2, year_bday2, None, None),
    (nametitle3, name3, surname3, day_bday3, month_bday3, year_bday3, None, None),
    (nametitle4, name4, surname4, day_bday4, month_bday4, year_bday4, None, None)
    ]
    for i, details in enumerate(passenger_details):
        booking.passenger_details[i].update_passenger_details(*details)
    return Redirect('/pay')

# Handle submission for 5 passengers
@rt('/passenger_details_submit5')
def passenger_details_submit5(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str,
                                nametitle3: str, name3: str, surname3: str, day_bday3: str, month_bday3: str, year_bday3: str,
                                nametitle4: str, name4: str, surname4: str, day_bday4: str, month_bday4: str, year_bday4: str,
                                nametitle5: str, name5: str, surname5: str, day_bday5: str, month_bday5: str, year_bday5: str):
    booking = controller.booking_list[0]
    passenger_details = [
    (nametitle1, name1, surname1, day_bday1, month_bday1, year_bday1, email1, phone_number1),
    (nametitle2, name2, surname2, day_bday2, month_bday2, year_bday2, None, None),
    (nametitle3, name3, surname3, day_bday3, month_bday3, year_bday3, None, None),
    (nametitle4, name4, surname4, day_bday4, month_bday4, year_bday4, None, None),
    (nametitle5, name5, surname5, day_bday5, month_bday5, year_bday5, None, None)
    ]
    for i, details in enumerate(passenger_details):
        booking.passenger_details[i].update_passenger_details(*details)
    return Redirect('/pay')

# Payment page
@rt('/pay')
def pay():
    return Div(
        themed_card(
            H1("เลือกช่องทางชำระเงิน"),
            Div(
                Button("📱 Online Banking", hx_get="/pay/onlineBanking", hx_target="#content", hx_swap="innerHTML"),
                Button("🏦 Debit Card", hx_get="/pay/debitCard", hx_target="#content", hx_swap="innerHTML"),
                Button("💳 Credit Card", hx_get="/pay/creditCard", hx_target="#content", hx_swap="innerHTML")
            )
        ),
        Div(id="content")
    )

# Online Banking Payment
@rt('/pay/onlineBanking')
def online_banking():
    paymentMethod = {"OnlineBanking"}
    return Div(
        themed_card(
            H1("ชำระเงินผ่าน Online Banking"),
            P("วิธีการชำระเงิน: Online Banking"),
            Img(src="https://yourdomain.com/online_banking_image.png"),
            Form(
                Button("ชำระเงิน", type="submit"), method="post", action="/onlineBanking_submit"
            )
        )
    )

@rt('/onlineBanking_submit')
def onlineBanking_submit_submit():
    onlineBanking = OnlineBanking()
    booking = controller.booking_list[0]
    booking.payment.process_payment(onlineBanking, booking.seat_list)
    booking.update_booking_status()
    return Redirect('/booking_confirm')

# Debit Card Payment
@rt('/pay/debitCard')
def debit_card():
    paymentMethod = {"DebitCard"}
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเดบิต"),
            P("วิธีการชำระเงิน: Debit Card"),
            Form(
                Label("Card Number", Input(type="text", id="debit_card_number", name="debit_card_number", required=True, placeholder="Enter card number")),
                Label("CVV", Input(type="password", id="debit_cvv", name="debit_cvv", required=True, placeholder="Enter CVV")),
                Label("EXP (MM/YY)", Input(type="text", id="debit_exp_date", name="debit_exp_date", required=True, placeholder="MM/YY")),
                Button("ชำระเงิน", type="submit"), method="post", action="/debitCard_submit"
            )
        )
    )

@rt('/debitCard_submit')
def debitCard_submit(debit_card_number: str, debit_cvv: str, debit_exp_date: str):
    debitCard = DebitCard(debit_card_number, debit_cvv, debit_exp_date)
    booking = controller.booking_list[0]
    booking.payment.process_payment(debitCard, booking.seat_list)
    booking.update_booking_status()
    return Redirect('/booking_confirm')

# Credit Card Payment
@rt('/pay/creditCard')
def credit_card():
    paymentMethod = {"CreditCard"}
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเครดิต"),
            P("วิธีการชำระเงิน: Credit Card"),
            Form(
                Label("Card Number", Input(type="text", id="credit_card_number", name="credit_card_number", required=True, placeholder="Enter card number")),
                Label("CVV", Input(type="password", id="credit_cvv", name="credit_cvv", required=True, placeholder="Enter CVV")),
                Label("EXP (MM/YY)", Input(type="text", id="credit_exp_date", name="credit_exp_date", required=True, placeholder="MM/YY")),
                Button("ชำระเงิน", type="submit"), method="post", action="/creditCard_submit"
            )
        )
    )

@rt('/creditCard_submit')
def CreditCard_submit(credit_card_number: str, credit_cvv: str, credit_exp_date: str):
    creditCard = CreditCard(credit_card_number, credit_cvv, credit_exp_date)
    booking = controller.booking_list[0]
    booking.payment.process_payment(creditCard, booking.seat_list)
    booking.update_booking_status()
    return Redirect('/booking_confirm')

# Confirmation
@rt('/booking_confirm')
def booking_confirm():
    return Redirect('/booking_details')

# Success Page
@rt('/success')
def success():
    return Div(
        themed_card(
            H1("🎉 จองตั๋วสำเร็จ!"),
            P("ขอบคุณที่ใช้บริการสายการบินของเรา"),
        )
    )

@rt('/booking_details')
def get():
    return Container(
                Form(
            Button("see submit", type="submit", style="font-sicontroller.booking_list[0]e: 16px; background-color: #ccc; padding: 10px;",
                   formaction="/booking_details_submit"),
            style="text-align: center; margin-top: -40px; padding: 20px;"
        )
    )

@rt('/booking_details_submit')
def get():
    container_content = [
        H1("submit", style="text-align: center; color: #FFFFFF; margin: 20px 0;")
    ]
    # Debugging: Print the passenger_num and passenger_list length

    passenger_num = controller.booking_list[0].passenger_count()
    booking = controller.booking_list[0]
    
    for i in range(passenger_num):
        passenger = controller.booking_list[0].passenger_details[i]
        print(f"Displaying info for passenger {i+1}: {passenger.name} {passenger.surname}")  # Log passenger details
        container_content.append(
            Card(
                H3("Profile Information", style="color: #ffee63;"),
                P(f"Name: {passenger.name}"),
                P(f"Surname: {passenger.surname}"),
                P(f"Birthday: {passenger.day_bday}"),
                P(f"Month: {passenger.month_bday}"),
                P(f"Year: {passenger.year_bday}"),
                P(f"Email: {passenger.email}"),
                P(f"Phone Number: {passenger.phone_number}"),
                P(f"Type: {passenger.passengerType.type}"),
                P(f"Seat: {passenger.seat.seat_id}"),
                P(f"Seat Status: {passenger.seat.seat_status}"),
                P(f"Booking Status: {booking.status}"),
                P(f"Pay By: {booking.payment.method.method_id}"),
                Form(
                    Button("Back", style="background-color: #ccc; padding: 10px; font-sicontroller.booking_list[0]e: 16px;", 
                        formaction="/booking_details")
                ),
                
                id="profile-card",
                style="border: 2px solid #fef5f3; border-radius: 10px; padding: 20px; margin: 10px;"
            )
        )
    
    # Ensure the content is being returned properly
    print(f"Returning container with {len(container_content)} cards.")  # Log the length of content to return

    return Container(*container_content)


# Run the app
serve()