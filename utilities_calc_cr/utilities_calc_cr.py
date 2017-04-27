import sys

import downloader
import parser

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 2:
        print 'usage: ./wordcount.py {--count | --topcount} file'
        sys.exit(1)

    option = sys.argv[1]
    #filename = sys.argv[2]
    if option == '--download':
        urls = []
        f = open('urls', 'r')
        for line in f:
            urls.append(line)
        print 'url', urls
        downloader.download_rates(urls, 'rates')
    elif option == '--readrates':
        parser.read_rates('rates')
    elif option == '--saverates':
        rates = parser.read_rates('rates')
        parser.save_rates(rates, 'rates', 'rates')
    elif option == '--getlogs':
        downloader.get_last_month_log('JxKdMWGdMViN2784OQb1', 'logs')
    elif option == '--logtodays':
        parser.log_to_days('logs', 'log')
    elif option == '--daystofdays':
        parser.days_to_formatted_days('logs/2017-03')
    elif option == '--getmaxpower':
        parser.load_dic_from_file('logs/2017-03', '2017-03-01.format')
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
