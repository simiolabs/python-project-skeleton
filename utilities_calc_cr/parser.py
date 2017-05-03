import os
import re
from datetime import datetime, timedelta
import time

KW_LOG = '.kw'

def read_rates(dirname, filename):
    """Read rates from file and return a list."""
    if os.path.exists(dirname + '/' + filename):
        print 'Reading...', filename
        f = open(dirname + '/' + filename, 'r')
        text = f.read()
        f.close()
        matches = re.findall(r'(\S+,\d+)</p>', text)
        if matches:
            matches[6] = matches[6][2:] #TODO dirty fix for html page error
            print matches
        return matches

def save_rates(dirname, filename, rates):
    """Take list of rates and save them to a file."""
    print 'Saving...', filename
    f = open(dirname + '/' + filename, 'w')
    for rate in rates:
        rate = rate.replace('.', '')
        rate = rate.replace(',', '.')
        f.write(rate + '\n')
    f.close()

def get_trr(dirname, filename):
    """Read TRR and return list."""
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
    """Read RR and return list."""
    if os.path.exists(dirname + '/' + filename):
        rate_list = []
        f = open(dirname + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[9:13]
        print rate_list
        return rate_list

def get_pr(dirname, filename):
    """Read PR and return list."""
    if os.path.exists(dirname + '/' + filename):
        rate_list = []
        f = open(dirname + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[13:]
        print rate_list
        return rate_list

def log_to_days(dirname, filename):
    """Take month long log file and divide it in day long log files."""
    if os.path.exists(dirname + '/' + filename):
        log_file = open(dirname + '/' + filename, 'r')
        print 'Saving daily logs...'
        for line in log_file:
            match = re.search(r'(\d+-\d+-\d+)', line)
            if match:
                month_log_dir = match.group(1)[:7]
                if not os.path.exists(dirname + '/' + month_log_dir):
                    print 'Creating...', month_log_dir
                    os.makedirs(dirname + '/' + month_log_dir)
                day_log_name = match.group(1)
                day_log_file = open(dirname + '/' + month_log_dir + '/' + \
                                    day_log_name, 'a')
                day_log_file.write(line)
                day_log_file.close()
        log_file.close()

def extract_time_and_power(dirname):
    """Take day long log file, extract timestamp and real power and save it."""
    if os.path.exists(dirname):
        paths = os.listdir(dirname)
        paths = sorted(paths)
        for path in paths:
            data_dic = {}
            print 'Reading:', path
            day_log_file = open(dirname + '/' + path, 'r')
            for line in day_log_file:
                match = re.search(r'\"real_power\":\"(\d+.\d+)\"\S+\"timestamp\":\"\S+T(\d+:\d+:\d+)', line)
                if match:
                    data_dic[match.group(2)] = match.group(1)
            day_log_file.close()
            new_file_name = path  + KW_LOG
            print 'Saving', new_file_name
            save_dic_to_file(dirname, new_file_name, data_dic)

def save_dic_to_file(dirname, filename, data_dic):
    """Save a key (timestamp) sorted dic to a file."""
    if os.path.exists(dirname):
        sorted_keys = sorted(data_dic)
        f = open(dirname + '/' + filename, 'w')
        for key in sorted_keys:
            f.write(key + ' ' + data_dic[key] + '\n')
        f.close()

def load_dic_from_file(dirname, filename):
    """Load a dic from a file, use first column as key."""
    if os.path.exists(dirname + '/' + filename):
        data_dic = {}
        f = open(dirname + '/' + filename, 'r')
        for line in f:
            data = line.strip('\n').split(' ')
            data_dic[data[0]] = data[1]
        f.close()
        return data_dic

def get_max_power(data_dic):
    """Print out max real power value."""
    print max(data_dic, key=data_dic.get), max(data_dic.values())

def convert_w_to_wh(data_dir):
    """
    Take a dic with a timestamp and kW, calculate kWh and return everything
    in a dic.
    """
    sorted_keys = sorted(data_dir.keys())
    i = 0
    while sorted_keys[i] is not sorted_keys[-1]:
        temp_list = []
        t1 = time.strptime(sorted_keys[i], '%H:%M:%S') # create time object from key
        t2 = time.strptime(sorted_keys[i + 1], '%H:%M:%S') # create time object from next key
        s1 = timedelta(hours=t1.tm_hour,minutes=t1.tm_min,seconds=t1.tm_sec).total_seconds() # convert t1 to secs
        s2 = timedelta(hours=t2.tm_hour,minutes=t2.tm_min,seconds=t2.tm_sec).total_seconds() # convert t2 to secs
        t_delta = s2 - s1
        kwh = float(data_dir[sorted_keys[i]]) * t_delta / 3600
        temp_list.append(data_dir[sorted_keys[i]])
        temp_list.append(str(t_delta))
        temp_list.append(str(kwh))
        data_dir[sorted_keys[i]] = temp_list
        i += 1
    return data_dir

def get_watts_hour(dirname):
    """Take day long log file, extract timestamp and real power and save it."""
    if os.path.exists(dirname):
        paths = os.listdir(dirname)
        paths = sorted(paths)
        for path in paths:
            if path.endswith():
                pass
