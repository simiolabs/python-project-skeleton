import time
import os
import parser
#CNFL

TRR = 'trr'
TR = 'tr'
TP = 'tp'

PEAK_TIME =             0
OFF_PEAK_TIME =         1
NIGHT_TIME =            2

#times
start_off_peak_time1 = time.strptime('06:01:00', '%H:%M:%S')
end_off_peak_time1   = time.strptime('10:00:59', '%H:%M:%S')
start_peak_time1    = time.strptime('10:01:00', '%H:%M:%S')
end_peak_time1      = time.strptime('12:30:59', '%H:%M:%S')
start_off_peak_time2 = time.strptime('12:31:00', '%H:%M:%S')
end_off_peak_time2   = time.strptime('17:30:59', '%H:%M:%S')
start_peak_time2    = time.strptime('17:31:00', '%H:%M:%S')
end_peak_time2      = time.strptime('20:00:59', '%H:%M:%S')
start_night_time1   = time.strptime('20:01:00', '%H:%M:%S')
end_night_time1     = time.strptime('23:59:59', '%H:%M:%S')
start_night_time2   = time.strptime('00:00:00', '%H:%M:%S')
end_night_time2     = time.strptime('06:00:59', '%H:%M:%S')

#TIME RESIDENTIAL RATE
TRR_LOW =               0
TRR_MID =               1
TRR_HIGH =              2

#power segments in kWh
TRR_LOW_POWER =         300
TRR_HIGH_POWER =        500

#RESIDENTIAL RATE
RR_FIXED =              0
RR_LOW =                1
RR_MID =                2
RR_HIGH =               3

#power segments in kWh
RR_FIXED_CHARGE =       30
RR_LOW_POWER =          200
RR_HIGH_POWER =         300

#PREFERENTIAL RATE
PR_E_LOW =              0
PR_P_LOW =              1
PR_MID =                2
PR_E_HIGH =             3
PR_P_HIGH =             4

PR_ENERGY =             0
PR_POWER =              1

#power segments in kWh
PR_LOW_POWER =          8
PR_MID_POWER =          30
PR_HIGH_POWER =         3000

#fire department tribute
FIRE_DEP_TRIBUTE =      0.075
FIRE_DEP_TAX =          1.750

#street lighting tribute
STREET_LIGHT_TRIBUTE =  3.51

#files
SEG_FILE = 'trr.seg'


#determine segment according to time
def get_time_segment_trr(timestamp):
    ts = time.strptime(timestamp, '%H:%M:%S')
    #peak time
    if ((ts >= start_peak_time1 and ts <= end_peak_time1) or
        (ts >= start_peak_time2 and ts <= end_peak_time2)):
        return PEAK_TIME
    #off_peak time
    elif ((ts >= start_off_peak_time1 and ts <= end_off_peak_time1) or
          (ts >= start_off_peak_time2 and ts <= end_off_peak_time2)):
        return OFF_PEAK_TIME
    #night time
    elif ((ts >= start_night_time1 and ts <= end_night_time1) or
         (ts >= start_night_time2 and ts <= end_night_time2)):
        return NIGHT_TIME
    else:
        return -1

def get_time_segments_day_totals_trr(dirname):
    if os.path.exists(dirname):
        paths = os.listdir(dirname)
        paths = sorted(paths)
        trr_seg_dic = {}
        for path in paths:
            if path.endswith(parser.KWH_LOG):
                off_peak_total, peak_total, night_total = (0 for i in range(3))
                print 'Reading...', path
                data_dic = parser.load_dic_from_file(dirname, path)
                sorted_keys = sorted(data_dic)
                for key in sorted_keys:
                    segment = get_time_segment_trr(key)
                    if segment is PEAK_TIME:
                        peak_total += float(data_dic[key][0])
                    elif segment is OFF_PEAK_TIME:
                        off_peak_total += float(data_dic[key][0])
                    elif segment is NIGHT_TIME:
                        night_total += float(data_dic[key][0])
                #print 'op', off_peak_total, 'p', peak_total, 'n', night_total
                key = path[:-4]
                temp_list = []
                temp_list.append(str(peak_total))
                temp_list.append(str(off_peak_total))
                temp_list.append(str(night_total))
                trr_seg_dic[key] = temp_list
        print 'Segment totals saved in:', SEG_FILE
        parser.save_dic_to_file(dirname, SEG_FILE, trr_seg_dic)

#determine consumption segment according to watts
def get_consumption_segment_trr(watts):
    if (watts <= TRR_LOW_POWER):
        return TRR_LOW
    elif (watts > TRR_LOW_POWER and watts <= TRR_HIGH_POWER):
        return TRR_MID
    elif (watts > TRR_HIGH_POWER):
        return TRR_HIGH
    else:
        return -1
#TODO integrate these three following functions into one, they all do the same
def calculate_peak_cost_trr(total_watts, costs_list):
    peak_cost = 0
    watts = 0
    if get_consumption_segment_trr(total_watts) is TRR_HIGH:
        watts = total_watts - float(TRR_HIGH_POWER)
        peak_cost += watts * float(costs_list[TRR_HIGH][PEAK_TIME])
        total_watts -= watts
        print 'cost2', peak_cost, 'watts2', watts, 'totalwatts', total_watts
    if get_consumption_segment_trr(total_watts) is TRR_MID:
        watts = total_watts - float(TRR_LOW_POWER)
        peak_cost += watts * float(costs_list[TRR_MID][PEAK_TIME])
        total_watts -= watts
        print 'cost1', peak_cost, 'watts1', watts, 'totalwatts', total_watts
    if get_consumption_segment_trr(total_watts) is TRR_LOW:
        watts = total_watts
        peak_cost += watts * float(costs_list[TRR_LOW][PEAK_TIME])
        total_watts -= watts
        print 'cost0', peak_cost, 'watts1', watts, 'total watts', total_watts
    return peak_cost

def calculate_off_peak_cost_trr(total_watts, costs_list):
    off_peak_cost = 0
    watts = 0
    if get_consumption_segment_trr(total_watts) is TRR_HIGH:
        watts = total_watts - float(TRR_HIGH_POWER)
        off_peak_cost += watts * float(costs_list[TRR_HIGH][OFF_PEAK_TIME])
        total_watts -= watts
        print 'cost2', off_peak_cost, 'watts2', watts, 'totalwatts', total_watts
    if get_consumption_segment_trr(total_watts) is TRR_MID:
        watts = total_watts - float(TRR_LOW_POWER)
        off_peak_cost += watts * float(costs_list[TRR_MID][OFF_PEAK_TIME])
        total_watts -= watts
        print 'cost1', off_peak_cost, 'watts1', watts, 'totalwatts', total_watts
    if get_consumption_segment_trr(total_watts) is TRR_LOW:
        watts = total_watts
        off_peak_cost += watts * float(costs_list[TRR_LOW][OFF_PEAK_TIME])
        total_watts -= watts
        print 'cost0', off_peak_cost, 'watts1', watts, 'totalwatts', total_watts
    return off_peak_cost

def calculate_night_cost_trr(total_watts, costs_list):
    night_cost = 0
    watts = 0
    if get_consumption_segment_trr(total_watts) is TRR_HIGH:
        watts = total_watts - float(TRR_HIGH_POWER)
        night_cost += watts * float(costs_list[TRR_HIGH][NIGHT_TIME])
        total_watts -= watts
        print 'cost2', night_cost, 'watts2', watts, 'totalwatts', total_watts
    if get_consumption_segment_trr(total_watts) is TRR_MID:
        watts = total_watts - float(TRR_LOW_POWER)
        night_cost += watts * float(costs_list[TRR_MID][NIGHT_TIME])
        total_watts -= watts
        print 'cost1', night_cost, 'watts1', watts, 'totalwatts', total_watts
    if get_consumption_segment_trr(total_watts) is TRR_LOW:
        watts = total_watts
        night_cost += watts * float(costs_list[TRR_LOW][NIGHT_TIME])
        total_watts -= watts
        print 'cost0', night_cost, 'watts1', watts, 'totalwatts', total_watts
    return night_cost

def calculate_time_segments_costs_trr(dirname):
    if os.path.exists(dirname):
        total_list = []
        off_peak_total, peak_total, night_total = (0 for i in range(3))
        print 'Reading...', SEG_FILE
        data_dic = parser.load_dic_from_file(dirname, SEG_FILE)
        sorted_keys = sorted(data_dic)
        for key in sorted_keys:
            peak_total += float(data_dic[key][PEAK_TIME]) / 1000
            off_peak_total += float(data_dic[key][OFF_PEAK_TIME]) / 1000
            night_total += float(data_dic[key][NIGHT_TIME]) / 1000
        total_list.append(peak_total)
        total_list.append(off_peak_total)
        total_list.append(night_total)
        #print total_list
        return total_list

def get_rates_trr(dirname, filename):
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

        #print twod_list
        return twod_list

def calculate_total_cost_trr(dirname, plan):
    if os.path.exists(dirname):
        off_peak_cost, peak_cost, night_cost = (0 for i in range(3))
        totals_list = calculate_time_segments_costs_trr(dirname)
        print totals_list
        #TODO these should be global variables
        costs_list = get_rates_trr('rates', 'rates-CNFL')
        print costs_list
        if plan is TRR:
            peak_cost = calculate_peak_cost_trr(totals_list[0], costs_list)
            off_peak_total = calculate_off_peak_cost_trr(totals_list[1], \
                                                         costs_list)
            night_total = calculate_night_cost_trr(totals_list[2], costs_list)

#determine consumption segment according to watts
def get_consumption_segment_rr(watts):
    if (watts <= RR_FIXED_CHARGE):
        return RR_FIXED
    elif (watts > RR_FIXED_CHARGE and watts <= RR_LOW_POWER):
        return RR_LOW
    elif (watts > RR_LOW_POWER and watts <= RR_HIGH_POWER):
        return RR_MID
    elif (watts > RR_HIGH_POWER):
        return RR_HIGH
    else:
        return -1

def get_rates_rr(dirname, filename):
    """Read RR and return list."""
    if os.path.exists(dirname + '/' + filename):
        rate_list = []
        f = open(dirname + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[9:13]
        #print rate_list
        return rate_list

#determine consumption segment according to watts and plan
def get_consumption_segment_pr(watts, plan):
    if (watts <= PR_LOW_POWER and plan == PR_ENERGY):
        return PR_E_LOW
    elif (watts <= PR_LOW_POWER and plan == PR_POWER):
        return PR_P_LOW
    elif (watts > PR_LOW_POWER and watts <= PR_HIGH_POWER):
        return PR_MID
    elif (watts > PR_HIGH_POWER and plan == PR_ENERGY):
        return PR_E_HIGH
    elif (watts > PR_HIGH_POWER and plan == PR_POWER):
        return PR_P_HIGH
    else:
        return -1

def get_rates_pr(dirname, filename):
    """Read PR and return list."""
    if os.path.exists(dirname + '/' + filename):
        rate_list = []
        f = open(dirname + '/' + filename, 'r')
        rate_list = f.read().splitlines()
        rate_list = rate_list[13:]
        #print rate_list
        return rate_list

#fire department tribute
def get_fire_department_tribute(total_watts, total_cost, plan):
    if (plan == 'TRR' or plan == 'RR' or plan == 'PR'):
        return (total_cost * FIRE_DEP_TRIBUTE)
    else:
        return (total_cost / total_watts * FIRE_DEP_TAX * FIRE_DEP_TRIBUTE)

#street lighting tribute
def get_street_lighting_tribute(total_watts):
    return (total_watts * STREET_LIGHT_TRIBUTE)
