class Controller:
   def __init__(self):
      self.is_logged_in = False
      self.account_list = []
      
   def turn_into_system(self, user):
      if not user.has_account():
         self.account.register()
         if self.account.is_success():
            print("Register successful")
         return self.auto_path_to_login(user)
      else:
         self.account.login()
         if self.account.is_correct():
               print("Login successful")
               self.is_logged_in = True
               self.display_home_page()

   def auto_path_to_login(self, user):
      self.account.login()
      if self.account.is_correct():
         print("Login successful")
         self.is_logged_in = True
         self.display_home_page()

   def display_home_page(self):
      print("Displaying home page")

class Userdetail:
   def __init__(self, firstname, lastname, birthday, gender, identification, nationality, phone_number, address, point):
      self.firstname = firstname
      self.lastname = lastname
      self.birthday = birthday
      self.gender = gender
      self.identification = identification
      self.nationality = nationality
      self.phone_number = phone_number
      self.address = address
      self.point = point

   def editprofile(self, firstname=None, lastname=None, birthday=None, gender=None, identification=None, nationality=None, phone_number=None, address=None, point=None):
      if firstname: self.firstname = firstname
      if lastname: self.lastname = lastname
      if birthday: self.birthday = birthday
      if gender: self.gender = gender
      if identification: self.identification = identification
      if nationality: self.nationality = nationality
      if phone_number: self.phone_number = phone_number
      if address: self.address = address
      if point: self.point = point

   # def calculate_points(self, transactions):
   #    total_points = 0
   #    for transaction in transactions:
   #       total_points += transaction['amount'] * 0.1  # Assuming 10% of transaction amount is converted to points
   #    self.point += total_points
   #    return total_points
      
   # def usepoint(self, points):
   #    if self.point >= points:
   #       self.point -= points
   #       return True
   #    return False

class Account:
   def __init__(self, email, password):
      self.email = email
      self.password = password
      self.purchased_history = []
      self.userdetail = None

   def login(self):
      print("Login Page")
      pass
      # Implement login logic
   
   def register(self, email, password, userdetail):
      print("Registering user")
      self.email = email
      self.password = password
      self.userdetail = userdetail
      # Implement registration logic
   
   def forgotpass(self):
      print("Forgot Password Page")
      pass
      # Implement forgot password logic
   
   def is_correct(self):
      # Implement validation
      return True
   
   def is_success(self):
      # Check if registration was successful
      return True
   
   def return_home_page(self):
      print("Returning Home Page")
      pass

class User:
   def __init__(self, username, password):
      self.username = username
      self.password = password
      self.account_created = False
   
   def has_account(self):
      return self.account_created