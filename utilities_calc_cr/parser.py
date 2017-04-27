import os
import re

def read_rates(dirname):
    if os.path.exists(dirname + '/page0.html'):
        f = open(dirname + '/page0.html', 'r')
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

def get_trr(dirname, filename):
    if os.path.exists(dirname + '/' + filename):
        rate_list = []
        f = open(dirname + '/' + filename, 'r')
        rate_list = f.read().splitlines()

        i = 0
        twod_list = [] #create 3x3 matrix
        for x in range (0, 3):
            new = []
            for y in range (0, 3):
                new.append(rate_list[i])
                i += 1
            twod_list.append(new)

        print twod_list
        return twod_list

def get_rr(dirname, filename):
    if os.path.exists(dirname + '/' + filename):
        rate_list = []
        f = open(dirname + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[9:13]
        print rate_list
        return rate_list

def get_pr(dirname, filename):
    if os.path.exists(dirname + '/' + filename):
        rate_list = []
        f = open(dirname + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[13:]
        print rate_list
        return rate_list

def log_to_days(dirname, filename):
    if os.path.exists(dirname + '/' + filename):
        log_file = open(dirname + '/' + filename, 'r')
        for line in log_file:
            match = re.search(r'(\d+-\d+-\d+)', line)
            if match:
                month_log_name = match.group(1)[:7]
                if not os.path.exists(dirname + '/' + month_log_name):
                    os.makedirs(dirname + '/' + month_log_name)
                day_log_name = match.group(1)
                day_log_file = open(dirname + '/' + month_log_name + '/' + \
                                    day_log_name, 'a')
                day_log_file.write(line)
                day_log_file.close()
        log_file.close()

def days_to_formatted_days(dirname):
    if os.path.exists(dirname):
        paths = os.listdir(dirname)
        for path in paths:
            print 'Reading:', path
            day_log_file = open(dirname + '/' + path, 'r')
            for line in day_log_file:
                #match = re.search(r'(\d+:\d+:\d+)', line)
                match = re.search(r'\"real_power\":\"(\d+.\d+)\"\S+\"timestamp\":\"\S+T(\d+:\d+:\d+)', line)
                if match:
                    formated_file = open(dirname + '/' + path + '.format', 'a')
                    formated_file.write(match.group(2) + ' ' + match.group(1) \
                                        + '\n')
                    formated_file.close()
            day_log_file.close()

def load_dic_from_file(dirname, filename):
    data_dic = {}
    if os.path.exists(dirname + '/' + filename):
        day_log_file = open(dirname + '/' + filename, 'r')
        for line in day_log_file:
            data = line.strip('\n').split(' ')
            data_dic[data[0]] = data[1]
        day_log_file.close()
        #print data_dic
        return data_dic
