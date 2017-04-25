import os
import urllib
import re
import datetime

LOG_NAME = 'log'

def download_rates(urls, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    i = 0
    for url in urls:
        local_name = 'page%d.html' % i
        print 'Retrieving...', url,
        urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
        i += 1

def read_rates(dir):
    if os.path.exists(dir + '/page0.html'):
        f = open(dir + '/page0.html', 'r')
        text = f.read()
        f.close()
        matches = re.findall(r'(\S+,\d+)</p>', text)
        #TODO dirty fix for html page error
        if matches:
            matches[6] = '180,78'
            print matches
        return matches

def save_rates(rates, dest_dir, filename):
    f = open(dest_dir + '/' + filename, 'w')
    for rate in rates:
        rate = rate.replace('.', '')
        rate = rate.replace(',', '.')
        f.write(rate + '\n')
    f.close()

def get_trr(dir, filename):
    if os.path.exists(dir + '/' + filename):
        rate_list = []
        f = open(dir + '/' + filename, 'r')
        rate_list = f.read().splitlines()

        i = 0
        twod_list = []
        for x in range (0, 3):
            new = []
            for j in range (0, 3):
                new.append(rate_list[i])
                i += 1
            twod_list.append(new)

        print twod_list
        return twod_list

def get_rr(dir, filename):
    if os.path.exists(dir + '/' + filename):
        rate_list = []
        f = open(dir + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[9:13]
        print rate_list
        return rate_list

def get_pr(dir, filename):
    if os.path.exists(dir + '/' + filename):
        rate_list = []
        f = open(dir + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[13:]
        print rate_list
        return rate_list

def download_old_log(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    local_name = 'log'
    print 'Retrieving...'
    urllib.urlretrieve('http://data.sparkfun.com/output/JxKdMWGdMViN2784OQb1.json?gte[timestamp]=03-01-2017&lt[timestamp]=04-01-2017&eq[name]=total', os.path.join(dest_dir, local_name))

def get_last_month_log(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    this_month = datetime.date.today()
    if this_month.month is 1:
        this_month = this_month.replace(day=1)
        last_month = this_month.replace(day=1, month=12)
    else:
        this_month = this_month.replace(day=1)
        last_month = this_month.replace(day=1, month=this_month.month - 1)
    end_month = this_month.strftime('%m-%d-%Y')
    start_month = last_month.strftime('%m-%d-%Y')

    local_name = LOG_NAME
    url = 'http://data.sparkfun.com/output/JxKdMWGdMViN2784OQb1.json?gte[timestamp]='+start_month+'&lt[timestamp]='+end_month+'&eq[name]=total'
    print 'Retrieving...'
    try:
        urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
    except Exception, e:
        print e
