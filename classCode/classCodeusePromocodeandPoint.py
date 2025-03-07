
class Account:
    def __init__(self, password, email, purchased_history, user_detail):
        self.password = password
        self.email = email
        self.purchased_history = purchased_history
        self.user_detail = user_detail


    def get_promocode(self):
        return self.user_detail.get_promocode()

    def use_points(self, points):
        if self.user_detail.point >= points:
            self.user_detail.point -= points
            return True
        return False
    
class Promocode:
    def __init__(self, code, discount_percent, expiration_date):
        self.code = code
        self.discount_percent = discount_percent
        self.expiration_date = expiration_date

    def is_valid(self):
        return True

    def get_available_promocode(self):
        pass

    def exchange_to_promocode (self):
        pass

    def all_promocode (self):
        pass
