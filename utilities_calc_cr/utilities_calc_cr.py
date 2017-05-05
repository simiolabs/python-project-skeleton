import sys

import downloader
import parser
import users

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 2:
        print 'usage: ./wordcount.py {--count | --topcount} file'
        sys.exit(1)

    option = sys.argv[1]
    #filename = sys.argv[2]
    if option == '--getrates':
        downloader.download_rates('urls', 'rates')
    elif option == '--parserates':
        parser.read_rates('rates', 'page0.html')
    elif option == '--saverates':
        rates_list = parser.read_rates('rates', 'page0.html')
        parser.save_rates('rates', 'rates-CNFL', rates_list)
    elif option == '--readrates':
        parser.get_trr('rates', 'rates-CNFL')
        parser.get_rr('rates', 'rates-CNFL')
        parser.get_pr('rates', 'rates-CNFL')
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
        user.assign_company('electricity', 'cnfl')
        user.assign_company('water', 'aya')
        user.print_info()
        user.create_account()
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
