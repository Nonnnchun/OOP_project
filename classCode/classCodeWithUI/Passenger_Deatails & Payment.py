from fasthtml.common import *

app, rt = fast_app()

def themed_card(*children):
   return Container(
      Card(
         *children,
      ),
      style="max-width: 1050px; margin: 0 auto; padding: 10px;"
   )

passenger_num = 1

# @rt('/passenger_details')
@rt('/')
def get():  
   if passenger_num == 1:
      return Redirect('/one_passenger')
   elif passenger_num == 2:
      return Redirect('/two_passenger')
   elif passenger_num == 3:
      return Redirect('/three_passenger')
   elif passenger_num == 4:
      return Redirect('/four_passenger')
   elif passenger_num == 5:
      return Redirect('/five_passenger')

@rt('/one_passenger')
def one_passenger():
   return Div(
      themed_card(
         H1("✈️ จองเที่ยวบิน AIRXXX"),
         
         Form(
               Grid(
                  Label("คำนำหน้า",
                     Select(
                           Option("นาย", value="นาย"),
                           Option("นาง", value="นาง"),
                           Option("นางสาว", value="นางสาว"),
                           id="nametitle1"
                     )
                  ),
                  Label("ชื่อ", Input(type="text", id="name1", required=True, placeholder="กรอกชื่อ")),
                  Label("นามสกุล", Input(type="text", id="surname1", required=True, placeholder="กรอกนามสกุล")),
               ),
               Grid(
                  Label("วันเกิด",
                     Select(
                     *[Option(i, value=i) for i in range(1, 32)],  # สร้าง Option จาก 1 ถึง 31
                     id="day_bday1"
                     )
                  ),
                  Label("เดือน",
                     Select(
                     *[Option(i, value=i) for i in range(1, 13)],  # สร้าง Option จาก 1 ถึง 31
                     id="month_bday1"
                     )
                  ),
                  Label("ปี",
                     Select(
                     *[Option(i, value=i) for i in range(1900, 2026)],  # สร้าง Option จาก 1 ถึง 31
                     id="year_bday1"
                     )
                  ),
               ),
               Grid(
                  Label("Email", Input(type="email", id="email1", required=True, placeholder="กรอก E-mail")),
                  Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
               ),
               Button("ถัดไป", type="submit"),
               method="post",
               action="/passenger_details_submit1"
         )
      ),
   )

@rt('/passenger_details_submit1')
def post(nametitle1 : str, name1: str, surname1: str, email1: str, phone_number1: str):
   return Redirect('/pay')

@rt('/two_passenger')
def two_passenger():
   return Div(
      themed_card(
         H1("✈️ จองเที่ยวบิน AIRXXX"),
         
         Form(
               Grid(
                  Label("คำนำหน้า",
                     Select(
                           Option("นาย", value="นาย"),
                           Option("นาง", value="นาง"),
                           Option("นางสาว", value="นางสาว"),
                           id="nametitle1"
                     )
                  ),
                  Label("ชื่อ", Input(type="text", id="name1", required=True, placeholder="กรอกชื่อ")),
                  Label("นามสกุล", Input(type="text", id="surname1", required=True, placeholder="กรอกนามสกุล")),
               ),
               Grid(
                  Label("วันเกิด",
                     Select(
                     *[Option(i, value=i) for i in range(1, 32)], id="day_bday1"
                     )
                  ),
                  Label("เดือน",
                     Select(
                     *[Option(i, value=i) for i in range(1, 13)], id="month_bday1"
                     )
                  ),
                  Label("ปี",
                     Select(
                     *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday1"
                     )
                  ),
               ),
               Grid(
                  Label("Email", Input(type="email", id="email1", required=True, placeholder="กรอก E-mail")),
                  Label("เบอร์โทรศัพท์", Input(type="text", id="phone_number1", required=True, placeholder="กรอกเบอร์โทรศัพท์")),
               ),
               Button("ถัดไป", type="submit"),
               method="post",
               action="/passenger_details_submit1"
         )
         ,
         Form(
               Grid(
                  Label("คำนำหน้า",
                     Select(
                           Option("นาย", value="นาย"),
                           Option("นาง", value="นาง"),
                           Option("นางสาว", value="นางสาว"),
                           id="nametitle2"
                     )
                  ),
                  Label("ชื่อ", Input(type="text", id="name2", required=True, placeholder="กรอกชื่อ")),
                  Label("นามสกุล", Input(type="text", id="surname2", required=True, placeholder="กรอกนามสกุล")),
               ),
               Grid(
                  Label("วันเกิด",
                     Select(
                     *[Option(i, value=i) for i in range(1, 32)], id="day_bday2"
                     )
                  ),
                  Label("เดือน",
                     Select(
                     *[Option(i, value=i) for i in range(1, 13)], id="month_bday2"
                     )
                  ),
                  Label("ปี",
                     Select(
                     *[Option(i, value=i) for i in range(1900, 2026)], id="year_bday2"
                     )
                  ),
               ),
               
               Button("ถัดไป", type="submit"),
               method="post",
               action="/passenger_details_submit2"
         )
      ),
   )

@rt('/passenger_details_submit2')
def post(nametitle1 : str, name1: str, surname1: str, day_bday1:str, month_bday1: str, year_bday1: str, email1: str, phone_number1: str, nametitle2 : str, name2: str, surname2: str, day_bday2:str, month_bday2: str, year_bday2: str):
   return Redirect('/pay')

@rt('/pay')
def pay():
   return Div(
      themed_card(
         H1("เลือกช่องทางชำระเงิน"),
         Div(
               Button("📱 Online Banking", 
                     hx_get="/pay/onlineBanking", hx_target="#content", hx_swap="innerHTML"),
               Button("🏦 Debit Card", 
                     hx_get="/pay/DebitCard", hx_target="#content", hx_swap="innerHTML"),
               Button("💳 Credit Card", 
                     hx_get="/pay/CreditCard", hx_target="#content", hx_swap="innerHTML")
         )
      ),
      Div(id="content"),  # ช่องแสดงรายละเอียดที่เลือก
   )

@rt('/pay/onlineBanking')
def online_banking():
   paymentmethod = "Online Banking"  # กำหนดช่องทางการชำระเงิน
   return Div(
      themed_card(
         H1("ชำระเงินผ่าน Online Banking"),
         P(f"วิธีการชำระเงิน: {paymentmethod}"),
         Img(src="https://example.com/online_banking_image.png"),
         Form(
               Button("ชำระเงิน"),
               method="post",
               action="/booking_confirm"
         )
      ),
   )

@rt('/pay/DebitCard')
def debit_card():
   paymentmethod = "Debit Card"  # กำหนดช่องทางการชำระเงิน
   return Div(
      themed_card(
         H1("ชำระด้วยบัตรเดบิต"),
         P(f"วิธีการชำระเงิน: {paymentmethod}"),
         Form(
               Label("Card Number", Input(type="text", id="debit_card_number", required=True, placeholder="Enter card number")),
               Label("CVV", Input(type="password", id="debit_cvv", required=True, placeholder="Enter CVV")),
               Label("EXP (MM/YY)", Input(type="text", id="debit_exp_date", required=True, placeholder="MM/YY")),
               Button("ชำระเงิน"),
               method="post",
               action="/booking_confirm"
         )
      ),
   )

@rt('/pay/CreditCard')
def credit_card():
   paymentmethod = "Credit Card"  # กำหนดช่องทางการชำระเงิน
   return Div(
      themed_card(
         H1("ชำระด้วยบัตรเครดิต"),
         P(f"วิธีการชำระเงิน: {paymentmethod}"),
         Form(
               Label("Card Number", Input(type="text", id="credit_card_number", required=True, placeholder="Enter card number")),
               Label("CVV", Input(type="password", id="credit_cvv", required=True, placeholder="Enter CVV")),
               Label("EXP (MM/YY)", Input(type="text", id="credit_exp_date", required=True, placeholder="MM/YY")),
               Button("ชำระเงิน"),
               method="post",
               action="/booking_confirm"
         )
      ),
   )

@rt('/booking_confirm')
def booking_confirm():

   return Redirect('/success')

@rt('/success')
def success():
   return Div(
      themed_card(
         H1("🎉 จองตั๋วสำเร็จ!"),
         P("ขอบคุณที่ใช้บริการสายการบินของเรา")
      ),
   )

serve()