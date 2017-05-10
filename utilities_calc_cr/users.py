import os
import datetime
import downloader
import parser

utilities = [ 'electricity', 'water' ]
electric_companies = [ 'cnfl' ]
water_companies = [ 'aya' ]
db = [ 'phant' ]

USER_INFO = 'info'
ELECTRIC_DIR = 'electric'
WATER_DIR = 'water'

class User(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.electric_company = ''
        self.electric_db = ''
        self.electric_pk = ''
        self.water_company = ''
        self.water_db = ''
        self.water_pk = ''

    def assign_company(self, utility, company):
        if (utility is utilities[0] and company in electric_companies):
            self.electric_company = company
        elif (utility is utilities[1] and company in water_companies):
            self.water_company = company
        else:
            print 'Undefined %s company: %s' % (utility, company)

    def assign_electric_db(self, database, public_key):
        if database in db and public_key:
            self.electric_db = database
            self.electric_pk = public_key

    def assign_water_db(self, database, public_key):
        if database in db and public_key:
            self.water_db = database
            self.water_pk = public_key

    def print_info(self):
        print 'User:', self.user_id
        print 'Electricity company:', self.electric_company
        print 'Electricity DB:', self.electric_db
        print 'Electricity PK:', self.electric_pk
        print 'Water company:', self.water_company
        print 'Water DB:', self.water_db
        print 'Water PK:', self.water_pk

    def create_account(self):
        if not os.path.exists(self.user_id):
            os.makedirs(self.user_id)

        f = open(self.user_id + '/' + USER_INFO, 'w')
        f.write(self.user_id+ '\n')
        f.write(self.electric_company + ' ' + self.electric_db + ' ' + \
                self.electric_pk + '\n')
        f.write(self.water_company + ' ' + self.water_db + ' ' + \
                self.water_pk + '\n')
        f.close()

    def get_last_month_electric_log(self, dirname):
        if not os.path.exists(self.user_id + '/' + ELECTRIC_DIR):
            os.makedirs(self.user_id + '/' + ELECTRIC_DIR)

        if self.electric_db == db[0]:
            today = datetime.date.today()
            downloader.get_last_month_log(self.electric_pk, \
                                          self.user_id + '/' + \
                                          ELECTRIC_DIR + '/' +
                                          dirname)

    def log_to_days(self, dirname):
        if os.path.exists(self.user_id + '/' + ELECTRIC_DIR):
            today = datetime.date.today()
            parser.log_to_days(self.user_id + '/' + ELECTRIC_DIR  + '/' +
                               dirname,
                               downloader.LOG_NAME)
