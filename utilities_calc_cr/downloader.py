import os
import urllib
import re

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
        f.write(rate + '\n')
    f.close()
