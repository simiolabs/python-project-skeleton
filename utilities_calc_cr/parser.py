import os
import re

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
        twod_list = [] #create 3x3 matrix
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

def log_to_days(dir, filename):
    if os.path.exists(dir + '/' + filename):
        log_file = open(dir + '/' + filename, 'r')
        for line in log_file:
            match = re.search(r'(\d+-\d+-\d+)', line)
            if match:
                month_log_name = match.group(1)[:7]
                if not os.path.exists(dir + '/' + month_log_name):
                    os.makedirs(dir + '/' + month_log_name)
                day_log_name = match.group(1)
                day_log_file = open(dir + '/' + month_log_name + '/' + \
                                    day_log_name, 'a')
                day_log_file.write(line)
                day_log_file.close()
        log_file.close()

#def days_to_
