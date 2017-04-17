import sys

import downloader

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
        downloader.download_rates(urls, 'rates')
    elif option == '--topcount':
        print_top(filename)
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
