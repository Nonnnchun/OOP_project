from fasthtml.common import *

app, rt = fast_app()

def themed_card(*children):
    return Container(
        Card(*children), style="max-width: 1050px; margin: 0 auto; padding: 10px;"
    )

# Default passenger number
passenger_num = 2

@rt('/')
def get():
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
    
    
    
    
    return Redirect('/pay')

# Handle submission for 2 passengers
@rt('/passenger_details_submit2')
def passenger_details_submit2(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str):
    return Redirect('/pay')

# Handle submission for 3 passengers
@rt('/passenger_details_submit3')
def passenger_details_submit3(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str,
                                nametitle3: str, name3: str, surname3: str, day_bday3: str, month_bday3: str, year_bday3: str):
    return Redirect('/pay')

# Handle submission for 4 passengers
@rt('/passenger_details_submit4')
def passenger_details_submit4(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str,
                                nametitle3: str, name3: str, surname3: str, day_bday3: str, month_bday3: str, year_bday3: str,
                                nametitle4: str, name4: str, surname4: str, day_bday4: str, month_bday4: str, year_bday4: str):
    return Redirect('/pay')

# Handle submission for 5 passengers
@rt('/passenger_details_submit5')
def passenger_details_submit5(nametitle1: str, name1: str, surname1: str, day_bday1: str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str,
                                nametitle2: str, name2: str, surname2: str, day_bday2: str, month_bday2: str, year_bday2: str,
                                nametitle3: str, name3: str, surname3: str, day_bday3: str, month_bday3: str, year_bday3: str,
                                nametitle4: str, name4: str, surname4: str, day_bday4: str, month_bday4: str, year_bday4: str,
                                nametitle5: str, name5: str, surname5: str, day_bday5: str, month_bday5: str, year_bday5: str):
    return Redirect('/pay')

# Payment page
@rt('/pay')
def pay():
    return Div(
        themed_card(
            H1("เลือกช่องทางชำระเงิน"),
            Div(
                Button("📱 Online Banking", hx_get="/pay/onlineBanking", hx_target="#content", hx_swap="innerHTML"),
                Button("🏦 Debit Card", hx_get="/pay/DebitCard", hx_target="#content", hx_swap="innerHTML"),
                Button("💳 Credit Card", hx_get="/pay/CreditCard", hx_target="#content", hx_swap="innerHTML")
            )
        ),
        Div(id="content")
    )

# Online Banking Payment
@rt('/pay/onlineBanking')
def online_banking():
    return Div(
        themed_card(
            H1("ชำระเงินผ่าน Online Banking"),
            P("วิธีการชำระเงิน: Online Banking"),
            Img(src="https://yourdomain.com/online_banking_image.png"),
            Form(
                Button("ชำระเงิน", type="submit"), method="post", action="/booking_confirm"
            )
        )
    )

# Debit Card Payment
@rt('/pay/DebitCard')
def debit_card():
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเดบิต"),
            P("วิธีการชำระเงิน: Debit Card"),
            Form(
                Label("Card Number", Input(type="text", id="debit_card_number", name="debit_card_number", required=True, placeholder="Enter card number")),
                Label("CVV", Input(type="password", id="debit_cvv", name="debit_cvv", required=True, placeholder="Enter CVV")),
                Label("EXP (MM/YY)", Input(type="text", id="debit_exp_date", name="debit_exp_date", required=True, placeholder="MM/YY")),
                Button("ชำระเงิน", type="submit"), method="post", action="/booking_confirm"
            )
        )
    )

@rt('/pay/DebitCard_submit')
def DebitCard_submit(debit_card_number: str, debit_cvv: str, debit_exp_date: str):
    return Redirect('/booking_confirm')

# Credit Card Payment
@rt('/pay/CreditCard')
def credit_card():
    return Div(
        themed_card(
            H1("ชำระด้วยบัตรเครดิต"),
            P("วิธีการชำระเงิน: Credit Card"),
            Form(
                Label("Card Number", Input(type="text", id="credit_card_number", name="credit_card_number", required=True, placeholder="Enter card number")),
                Label("CVV", Input(type="password", id="credit_cvv", name="credit_cvv", required=True, placeholder="Enter CVV")),
                Label("EXP (MM/YY)", Input(type="text", id="credit_exp_date", name="credit_exp_date", required=True, placeholder="MM/YY")),
                Button("ชำระเงิน", type="submit"), method="post", action="/booking_confirm"
            )
        )
    )

@rt('/pay/CreditCard_submit')
def CreditCard_submit(credit_card_number: str, credit_cvv: str, credit_exp_date: str):
    return Redirect('/booking_confirm')

# Confirmation
@rt('/booking_confirm')
def booking_confirm():
    return Redirect('/success')

# Success Page
@rt('/success')
def success():
    return Div(
        themed_card(
            H1("🎉 จองตั๋วสำเร็จ!"),
            P("ขอบคุณที่ใช้บริการสายการบินของเรา"),
        )
        
    )

# Run the app
serve()
