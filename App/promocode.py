from fasthtml.common import *
from Backend import *
from commonstyle import *

app, rt = fast_app()
promocode_app = app 

@rt("/promocode")
def get():
    """หน้าแสดงโปรโมชั่น & แต้มของผู้ใช้"""
    return Title("Promotion Codes"), Container(
        Button("Back to Home", 
               hx_get="/home", 
               hx_target="body", 
               hx_swap="outerHTML",
               style="background-color: #FFFF33; color: black; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px; border: none; cursor: pointer; font-weight: bold;"),
        H1("Promotion Codes", cls="text-center mb-4"),
        Div(get_user_info(), id="user-info", cls="mb-4 p-3 border rounded"),
        H2("Available Promotions", cls="mb-3"),
        get_promotion_table(),
        Dialog(id="confirm-dialog", cls="p-4 rounded shadow-lg"),
        get_page_styles(),
        Script(""" 
            function closeDialog() { 
                document.getElementById('confirm-dialog').close(); 
            }
            
            function showToast(message, isSuccess = true) {
                const toast = document.createElement('div');
                toast.className = isSuccess ? 'toast success' : 'toast error';
                toast.textContent = message;
                document.body.appendChild(toast);
                
                setTimeout(() => {
                    toast.classList.add('show');
                }, 100);
                
                setTimeout(() => {
                    toast.classList.remove('show');
                    setTimeout(() => document.body.removeChild(toast), 300);
                }, 3000);
            }
        """)
    )


def get_page_styles():
    return Style("""
        .success { background-color: #4CAF50; color: white; }
        .error { background-color: #f44336; color: white; }
        .secondary { background-color: #363636; }
        
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 4px;
            transform: translateY(100px);
            opacity: 0;
            transition: transform 0.3s, opacity 0.3s;
            z-index: 1000;
        }
        
        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #FFFF33;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        button {
            padding: 8px 16px;
            margin: 5px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        button:hover {
            opacity: 0.8;
        }
        
        .code-badge {
            display: inline-block;
            padding: 4px 8px;
            margin: 3px;
            background-color: #FFFF33;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        .expired {
            text-decoration: line-through;
            opacity: 0.7;
        }
    """)

def get_user_info():
    """แสดงแต้มและโค้ดที่แลกแล้วของผู้ใช้"""
    return Div(
        Div(
            Span("Your Points: ", style="font-size: 16px;"),
            Span(f"{user_account.points}", style="font-size: 24px; font-weight: bold; color: #4CAF50;", id="user-points")
        ),
        H3("Your Redeemed Codes", cls="mt-3"),
        get_owned_codes_list(),
        id="update-section"
    )

# สมมติว่ามี user ที่ล็อกอินอยู่
user_account = UserDetail("John", "Doe", points=500)

def get_owned_codes_list():
    """แสดงโค้ดที่แลกแล้วของผู้ใช้"""
    if not user_account.promocode_list:  # ✅ ใช้ instance ของ user_account
        return P("You haven't redeemed any codes yet.", style="color: #777;")
    
    owned_code_list = []
    for code in user_account.promocode_list:  # ✅ ใช้ instance แทน property
        promo = next((p for p in promotion_codes if p.code == code), None)
        if promo:
            is_expired = promo.is_expired()
            cls = "code-badge" + (" expired" if is_expired else "")
            expired_text = " (EXPIRED)" if is_expired else ""
            owned_code_list.append(
                Div(
                    f"{code} : -{promo.discount_percent}% {expired_text}",
                    cls=cls
                )
            )
    
    return Div(*owned_code_list, id="owned-codes", cls="mt-2")


def get_promotion_table():
    """สร้างตารางแสดงโค้ดโปรโมชั่น"""
    promo_rows = []
    
    for promo in promotion_codes:
        # Check if code is already redeemed
        is_redeemed = promo.code in user_account.promocode_list
        is_expired = promo.is_expired()
        has_enough_points = user_account.points >= promo.points
        
        button_attrs = {}
        
        if is_redeemed:
            button_text = "Redeemed"
            button_cls = "secondary"
            button_disabled = True
        elif is_expired:
            button_text = "Expired"
            button_cls = "secondary"
            button_disabled = True
        elif not has_enough_points:
            button_text = "Not Enough Points"
            button_cls = "secondary"
            button_disabled = True
        else:
            button_text = "Redeem"
            button_cls = "success"
            button_disabled = False
            button_attrs = {
                "hx_get": f"/confirm-redeem/{promo.code}",
                "hx_target": "#confirm-dialog",
                "hx_swap": "outerHTML"
            }
        
        row_cls = "expired" if is_expired else ""
        
        promo_rows.append(
            Tr(
                Td(promo.description),
                Td(f"{promo.points} pts"),
                Td(f"{promo.discount_percent}%"),
                Td(promo.expiration_date),
                Td(
                    Button(
                        button_text,
                        cls=button_cls,
                        disabled=button_disabled,
                        **button_attrs
                    )
                ),
                cls=row_cls
            )
        )

    return Table(
        Thead(Tr(Th("Description"), Th("Points Required"), Th("Discount %"), Th("Expiration Date"), Th("Action"))),
        Tbody(*promo_rows),
        id="promo-table",
        cls="mt-4"
    )

@rt("/confirm-redeem/{code}")
def confirm_redeem(code: str):
    """แสดงป๊อปอัปยืนยันก่อนแลก"""
    promo = next((p for p in promotion_codes if p.code == code), None)

    if not promo:
        return Dialog(
            P("Error: Promotion code not found"),
            Button("Close", onclick="this.closest('dialog').close()"),
            open=True,
            id="confirm-dialog"
        )

    # เช็คว่าแต้มผู้ใช้เพียงพอหรือไม่
    if not promo.can_redeem(user_account.points):
        # ถ้าแต้มไม่เพียงพอหรือโค้ดหมดอายุ
        if promo.is_expired():
            message = f"This promotion code has expired on {promo.expiration_date}."
        else:
            message = f"You do not have enough points. You need {promo.points} points, but you have {user_account.points}."
            
        return Dialog(
            H3("Cannot Redeem", style="color: #f44336; margin-top: 0;"),
            P(message),
            Button("Close", onclick="this.closest('dialog').close()", cls="secondary"),
            open=True,
            id="confirm-dialog"
        )

    return Dialog(
        Div(
            P(f"Description: {promo.description}"),
            P(f"Discount: ", Span(f"{promo.discount_percent}%", style="color: #4CAF50; font-weight: bold;")),
            P(f"Points Required: ", Span(f"{promo.points}", style="font-weight: bold;")),
            P(f"Your Current Points: ", Span(f"{user_account.points}", style="font-weight: bold;")),
            P(f"Remaining Points After Redemption: ", 
              Span(f"{user_account.points - promo.points}", style="color: #1976D2; font-weight: bold;")),
            cls="mt-3 mb-3"
        ),
        P("Are you sure you want to redeem this promocode?"),
        Div(
            Button("Yes, Redeem", 
                  hx_post=f"/redeem/{promo.code}",  
                  hx_target="#update-section",  
                  hx_swap="outerHTML",
                  hx_on="htmx:afterRequest: closeDialog();",
                   cls="success"),
            Button("Cancel", onclick="this.closest('dialog').close()", cls="secondary"),
            style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;"
        ),
        open=True,
        id="confirm-dialog",
        style="max-width: 500px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
    )

@rt("/redeem/{code}")
def redeem(code: str):
    """ดำเนินการแลกโค้ด"""
    promo = next((p for p in promotion_codes if p.code == code), None)

    if not promo:
        return get_user_info(), Script("showToast('Promotion code not found', false);")

    # Create a new Promocode instance to avoid modifying the original
    promo_instance = Promocode(
        promo.code, 
        promo.points, 
        promo.discount_percent, 
        promo.expiration_date,
        promo.description
    )

    if user_account.redeem_promocode(promo_instance):
        # Return updated user info section และเพิ่ม Script แสดง toast ว่าสำเร็จ
        return get_user_info(), Script("""
            showToast('Promocode redeemed successfully!', true);
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        """)
    else:
        return get_user_info(), Script("showToast('Failed to redeem promocode', false);")
