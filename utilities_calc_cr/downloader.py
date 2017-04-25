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

def download_old_log(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    local_name = 'log'
    print 'Retrieving...'
    urllib.urlretrieve('http://data.sparkfun.com/output/JxKdMWGdMViN2784OQb1.json?gte[timestamp]=03-01-2017&lt[timestamp]=04-01-2017&eq[name]=total', os.path.join(dest_dir, local_name))

def get_last_month_log(public_key, dest_dir):
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
    url = 'http://data.sparkfun.com/output/'+public_key+'.json?gte[timestamp]='+start_month+'&lt[timestamp]='+end_month+'&eq[name]=total'
    print 'Retrieving...'
    try:
        urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
    except Exception, e:
        print e
