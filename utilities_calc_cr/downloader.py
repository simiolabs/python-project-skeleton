import os
import urllib
import urllib2
import re
import datetime
import time

LOG = '.log'
USER_AGENT = 'Utilities Calc CR'

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

def get_last_month_log(public_key, dest_dir, database):
    """Download last's month log and save it to a file."""
    this_month = datetime.date.today()
    if this_month.month is 1:
        this_month = this_month.replace(day=1)
        last_month = this_month.replace(day=1, month=12)
    else:
        this_month = this_month.replace(day=1)
        last_month = this_month.replace(day=1, month=this_month.month - 1)

    if database == 'phant':
        get_log_phant(public_key, dest_dir, last_month, this_month)
    elif database == 'emoncms':
        get_log_emoncms(public_key, dest_dir, last_month, this_month)

def get_log_phant(public_key, dest_dir, start_date, end_date):
    """Download log from Phant.io and save it to a file."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    end = end_date.strftime('%m-%d-%Y')
    start = start_date.strftime('%m-%d-%Y')
    local_name = start_date.strftime('%Y-%m' + LOG)
    #FIXME: name is hardcoded
    url = 'http://data.sparkfun.com/output/'+public_key+'.json?gte[timestamp]='+start+'&lt[timestamp]='+end+'&eq[name]=total'
    print 'Retrieving...', url
    try:
        urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
        print 'Saved in:', local_name
    except Exception, e:
        print e

def get_log_emoncms(public_key, dest_dir, start_date, end_date):
    """Download log from EmonCMS.org and save it to a file."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    end_ts = str(int(time.mktime(end_date.timetuple())) * 1000)
    start_ts = str(int(time.mktime(start_date.timetuple())) * 1000)
    local_name = start_date.strftime('%Y-%m' + LOG)
    #FIXME: node is hardcoded
    url = 'http://simiolabs.com/emoncms/feed/data.json?id=1&apikey='+public_key+'&start='+start_ts+'&end='+end_ts+'&interval=300'
    user_agent = USER_AGENT
    values = { }
    headers = {'User-Agent': user_agent}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    print 'Retrieving...', url
    try:
        response = urllib2.urlopen(req)
        f = open(dest_dir + '/' + local_name, 'w')
        f.write(response.read())
        f.close()
    except urllib2.URLError as e:
        print e.reason
