import os

utilities = [ 'electricity', 'water' ]
electricity_companies = [ 'cnfl' ]
water_companies = [ 'aya' ]

USER_INFO = 'info'
LOG_DIR = 'logs'

class User(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.electricity_company = ''
        self.water_company = ''

    def assign_company(self, utility, company):
        if (utility is utilities[0] and company in electricity_companies):
            self.electricity_company = company
        elif (utility is utilities[1] and company in water_companies):
            self.water_company = company
        else:
            print 'Undefined %s company: %s' % (utility, company)

    def print_info(self):
        print 'User: %s' % (self.user_id)
        print 'Electricity: %s' % (self.electricity_company)
        print 'Water: %s' % (self.water_company)

    def create_account(self):
        if not os.path.exists(self.user_id):
            os.makedirs(self.user_id)

        f = open(self.user_id + '/' + USER_INFO, 'a')
        f.write(self.user_id+ '\n')
        f.write(self.electricity_company+ '\n')
        f.write(self.water_company)
        f.close()
