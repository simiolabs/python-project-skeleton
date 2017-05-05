import os
import datetime
import downloader

utilities = [ 'electricity', 'water' ]
electricity_companies = [ 'cnfl' ]
water_companies = [ 'aya' ]
db = [ 'phant' ]

USER_INFO = 'info'
ELECTRIC_DIR = 'electric'
WATER_DIR = 'water'

class User(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.electricity_company = ''
        self.electricity_db = ''
        self.electricity_pk = ''
        self.water_company = ''
        self.water_db = ''
        self.water_pk = ''

    def assign_company(self, utility, company):
        if (utility is utilities[0] and company in electricity_companies):
            self.electricity_company = company
        elif (utility is utilities[1] and company in water_companies):
            self.water_company = company
        else:
            print 'Undefined %s company: %s' % (utility, company)

    def assign_electric_db(self, database, public_key):
        if database in db and public_key:
            self.electricity_db = database
            self.electricity_pk = public_key

    def assign_water_db(self, database, public_key):
        if database in db and public_key:
            self.water_db = database
            self.water_pk = public_key

    def print_info(self):
        print 'User:', self.user_id
        print 'Electricity company:', self.electricity_company
        print 'Electricity DB:', self.electricity_db
        print 'Electricity PK:', self.electricity_pk
        print 'Water company:', self.water_company
        print 'Water DB:', self.water_db
        print 'Water PK:', self.water_pk

    def create_account(self):
        if not os.path.exists(self.user_id):
            os.makedirs(self.user_id)

        f = open(self.user_id + '/' + USER_INFO, 'w')
        f.write(self.user_id+ '\n')
        f.write(self.electricity_company + ' ' + self.electricity_db + ' ' + \
                self.electricity_pk + '\n')
        f.write(self.water_company + ' ' + self.water_db + ' ' + \
                self.water_pk + '\n')
        f.close()

    def get_last_month_electric_log(self):
        if not os.path.exists(self.user_id + '/' + ELECTRIC_DIR):
            os.makedirs(self.user_id + '/' + ELECTRIC_DIR)

        if self.electricity_db == db[0]:
            today = datetime.date.today()
            downloader.get_last_month_log(self.electricity_pk, \
                                          self.user_id + '/' + \
                                          ELECTRIC_DIR + '/' +
                                          today.strftime('%Y-%m'))
