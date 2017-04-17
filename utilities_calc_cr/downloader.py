import os
import urllib

def download_rates(urls, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    i = 0
    for url in urls:
        local_name = 'page%d.html' % i
        print 'Retrieving...', url,
        urllib.urlretrieve(url, os.path.join(dest_dir, local_name))
        i += 1
