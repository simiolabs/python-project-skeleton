import sys

import datetime

import downloader
import parser
import users
import electric_CNFL

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 2:
        print 'usage: ./wordcount.py {--count | --topcount} file'
        sys.exit(1)

    today = datetime.date.today()
    last_month = today.replace(month=today.month - 1)
    str_last_month = last_month.strftime('%Y-%m')

    option = sys.argv[1]
    #filename = sys.argv[2]
    if option == '--getrates':
        electric = electric_CNFL.ElectricCNFL()
        electric.get_rates()
    elif option == '--getlog':
        downloader.get_last_month_log('JxKdMWGdMViN2784OQb1', 'logs')
    elif option == '--logtodays':
        parser.log_to_days('logs', 'log')
    elif option == '--getwatts':
        parser.extract_time_and_power('logs/2017-03')
    elif option == '--loaddic':
        load_dic = parser.load_dic_from_file('logs/2017-03', '2017-03-01.kw')
        print load_dic
        load_dic = parser.load_dic_from_file('logs/2017-03', '2017-03-01.kwh')
        print load_dic
    elif option == '--getmaxpower':
        data_dic = parser.load_dic_from_file('logs/2017-03', '2017-03-01.kw')
        parser.get_max_power(data_dic)
    elif option == '--getwattshour':
        parser.get_watts_hour('logs/2017-03')
    elif option == '--testuser':
        user = users.User('111650608')
        user.assign_company('electricity', 'cnfl', 'trr')
        user.assign_electric_db('phant', 'JxKdMWGdMViN2784OQb1')
        user.assign_company('water', 'aya', 'r')
        user.print_info()
        user.create_account()
        user.electric_get_last_month_log(str_last_month)
        user.electric_log_to_days(str_last_month)
        user.electric_extract_time_and_power(str_last_month)
        user.electric_get_watts_hour(str_last_month)
    elif option == '--calcbill':
        user = users.User('111650608')
        user.assign_company('electricity', 'cnfl', 'trr')
        user.assign_electric_db('phant', 'JxKdMWGdMViN2784OQb1')
        user.assign_company('water', 'aya', 'r')
        user.print_info()
        user.electric_get_total_cost_trr(str_last_month)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
