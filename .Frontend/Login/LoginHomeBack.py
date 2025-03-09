from fasthtml.common import *
from hmac import compare_digest


# ================================
#   ACCOUNT MANAGEMENT CLASSES
# ================================
class UserDetail:
   def __init__(self, firstname, lastname, points=0):
      # birthday, gender, identification, nationality, phone_number, address,
      self.__firstname = firstname
      self.__lastname = lastname
      self.__points = points
      self.__birthday = []
      self.__gender = []
      self.__identification = []
      self.__nationality = []
      self.__phone_number = []
      self.__address = []
      self.__promocode_list = []
   
   @property
   def firstname(self):
      return self.__firstname
   
   @property
   def lastname(self):
      return self.__lastname
   
   @property
   def points(self):
      return self.__points
   
   @property
   def birthday(self):
      return self.__birthday
   
   @property
   def gender(self):
      return self.__gender
   
   @property
   def identification(self):
      return self.__identification
   
   @property
   def nationality(self):
      return self.__nationality
   
   @property
   def phone_number(self):
      return self.__phone_number
   
   @property
   def address(self):
      return self.__address
   
   @property
   def promocode_list(self):
      return self.__promocode_list
   
   def edit_profile(self, firstname=None, lastname=None, phone_number=None, address=None):
      if firstname:
         self.__firstname = firstname
      if lastname:
         self.__lastname = lastname
      if phone_number:
         self.__phone_number = phone_number
      if address:
         self.__address = address

class Account:
   def __init__(self, email, password, userdetail):
      self.__email = email
      self.__password = password
      self.__userdetail = userdetail

   @property
   def email(self):
      return self.__email

   @property
   def userdetail(self):
      return self.__userdetail
   
   def check_password(self, password):
      return compare_digest(self.__password, password)
   
   def change_password(self, old_password, new_password, confirm_new_password):
         if new_password != confirm_new_password:
            return "New passwords do not match"
         if len(new_password) < 6:  # Ensure new password is strong
            return "New password must be at least 6 characters long"

         self.__password = new_password
         return "Password changed successfully"

# Controller to manage users
class Controller:
   def __init__(self):
      self.__accounts = []  # List of registered accounts
      self.__logged_in_user = None  # Store currently logged-in user
   
   def register(self, email, password, firstname, lastname):
      if any(acc._Account__email == email for acc in self.__accounts):
         return "Email already registered!"
      
      user_detail = UserDetail(firstname, lastname)
      new_account = Account(email, password, user_detail)
      self.__accounts.append(new_account)
      return "Registration successful!"

   def login(self, email, password):
      for acc in self.__accounts:
         if acc._Account__email == email and acc.check_password(password):
               self.__logged_in_user = acc
               return "Login successful!"
      return "Invalid email or password!"

   def get_logged_in_user(self):
      return self.__logged_in_user
   
   def logout(self):
      self.__logged_in_user = None
      return "Logged out successfully!"

