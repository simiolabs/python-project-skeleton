import os
import urllib
import urllib2
import re
import datetime
import time

LOG = '.log'

def download_rates(filename, dest_dir):
    """Download rates from websites in list of urls."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    urls = []
    f = open(filename, 'r')
    for line in f:
        urls.append(line)
    f.close()
    #print 'urls', urls
    i = 0
    for url in urls:
        local_name = 'page%d.html' % i
        print 'Retrieving...', url
        try:
            urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
            i += 1
        except Exception, e:
            print e

def get_last_month_log(public_key, dest_dir):
    """Download last's month log from Phant.io and save it."""
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

    local_name = last_month.strftime('%Y-%m' + LOG)
    #FIXME: name is hardcoded
    url = 'http://data.sparkfun.com/output/'+public_key+'.json?gte[timestamp]='+start_month+'&lt[timestamp]='+end_month+'&eq[name]=total'
    print 'Retrieving...', url
    try:
        urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
        print 'Saved in:', local_name
    except Exception, e:
        print e

def get_last_month_log_emoncms(public_key, dest_dir):
    """Download last's month log from EmonCMS and save it."""
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
    end_ts = str(int(time.mktime(this_month.timetuple())) * 1000)
    start_ts = str(int(time.mktime(last_month.timetuple())) * 1000)

    local_name = last_month.strftime('%Y-%m' + LOG)
    #url = 'https://emoncms.org/emoncms/feed/data.json?id=1&apikey='+public_key+'&start='+start_ts+'&end='+end_ts+'&interval=75'
    #url = 'http://simiolabs.com/emoncms/feed/data.json?id=1&apikey='+public_key+'&start='+start_ts+'&end='+end_ts+'&interval=300'
    #print 'Retrieving...', url
    #try:
    #    urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
    #    print 'Saved in:', local_name
    #except Exception, e:
    #    print e
    #FIXME: node is hardcoded
    url = 'http://simiolabs.com/emoncms/feed/data.json?id=1&apikey='+public_key+'&start='+start_ts+'&end='+end_ts+'&interval=300'
    user_agent = 'Utilities Calc CR'
    values = { }
    headers = {'User-Agent': user_agent}

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    try:
        response = urllib2.urlopen(req)
        f = open(dest_dir + '/' + local_name, 'w')
        f.write(response.read())
        f.close()
    except urllib2.URLError as e:
        print e.reason
