from fasthtml.common import *
from hmac import compare_digest


# ================================
#   ACCOUNT MANAGEMENT CLASSES
# ================================
class UserDetail:
   def __init__(self, firstname, lastname, points=0):
      self.firstname = firstname
      self.lastname = lastname
      self.points = points

class Account:
   def __init__(self, email, password, userdetail):
      self.email = email
      self.password = password
      self.userdetail = userdetail

   def check_password(self, password):
      return compare_digest(self.password, password)

# Controller to manage users
class Controller:
   def __init__(self):
      self.accounts = []  # List of registered accounts
      self.logged_in_user = None  # Store currently logged-in user

   def register(self, email, password, firstname, lastname):
      if any(acc.email == email for acc in self.accounts):
         return "Email already registered!"
      
      user_detail = UserDetail(firstname, lastname)
      new_account = Account(email, password, user_detail)
      self.accounts.append(new_account)
      return "Registration successful!"

   def login(self, email, password):
      for acc in self.accounts:
         if acc.email == email and acc.check_password(password):
               self.logged_in_user = acc
               return "Login successful!"
      return "Invalid email or password!"

   def get_logged_in_user(self):
      return self.logged_in_user

   def logout(self):
      self.logged_in_user = None

controller = Controller()
