import time
import os
import downloader
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
#TODO some of them should be global for every file to see them
URLS_FILE =             'urls'
RATES_HTML =            'page0.html'
RATES_FOLDER =          'rates'
RATES_FILE =            'rates-CNFL'
SEG_FILE =              'trr.seg'


class ElectricCNFL(object):
    def __init__(self):
        pass

    def get_rates(self):
        downloader.download_rates(URLS_FILE, RATES_FOLDER)
        rates_list = parser.read_rates(RATES_FOLDER, RATES_HTML)
        parser.save_rates(RATES_FOLDER, RATES_FILE, rates_list)

    def get_fire_department_tribute(total_watts, total_cost, plan):
        """Calculate fire department tribute."""
        if (plan == 'TRR' or plan == 'RR' or plan == 'PR'):
            return (total_cost * FIRE_DEP_TRIBUTE)
        else:
            return (total_cost / total_watts * FIRE_DEP_TAX * FIRE_DEP_TRIBUTE)

    def get_street_lighting_tribute(total_watts):
        """Calculate street lighting tribute."""
        return (total_watts * STREET_LIGHT_TRIBUTE)

class TimeResidentialRate(ElectricCNFL):
    def __init__(self):
        pass

    def get_time_segment_trr(self, timestamp):
        """Determine segment according to time."""
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

    def get_time_segments_day_totals_trr(self, dirname):
        """Add all watts separated by time segments in file and save in a new file
        as: DATE PEAK_TOTAL OFF_PEAK_TOTAL NIGHT_TOTAL."""
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
                        segment = self.get_time_segment_trr(key)
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

    def get_consumption_segment_trr(self, watts):
        """Determine consumption segment according to watts."""
        if (watts <= TRR_LOW_POWER):
            return TRR_LOW
        elif (watts > TRR_LOW_POWER and watts <= TRR_HIGH_POWER):
            return TRR_MID
        elif (watts > TRR_HIGH_POWER):
            return TRR_HIGH
        else:
            return -1

    def get_time_segment_cost_trr(self, total_watts, costs_list, time_seg):
        """Calculate the cost of some watts according to it's time and consumption
        segment."""
        total_cost = 0
        watts = 0
        if self.get_consumption_segment_trr(total_watts) is TRR_HIGH:
            watts = total_watts - float(TRR_HIGH_POWER)
            total_cost += watts * float(costs_list[TRR_HIGH][time_seg])
            total_watts -= watts
            print 'cost2', total_cost, 'watts2', watts, 'total_w', total_watts
        if self.get_consumption_segment_trr(total_watts) is TRR_MID:
            watts = total_watts - float(TRR_LOW_POWER)
            total_cost += watts * float(costs_list[TRR_MID][time_seg])
            total_watts -= watts
            print 'cost1', total_cost, 'watts1', watts, 'total_w', total_watts
        if self.get_consumption_segment_trr(total_watts) is TRR_LOW:
            watts = total_watts
            total_cost += watts * float(costs_list[TRR_LOW][time_seg])
            total_watts -= watts
            print 'cost0', total_cost, 'watts1', watts, 'total_w', total_watts
        return total_cost

    def get_time_segments_totals_trr(self, dirname):
        """Read from a file all the daily time segmented totals, add them and return
        them in a list."""
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

    def get_rates_trr(self, dirname, filename):
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

    def get_total_cost_trr(self, dirname, plan):
        """Get the total costs for every segment, add them and return the result."""
        if os.path.exists(dirname):
            off_peak_cost, peak_cost, night_cost = (0 for i in range(3))
            totals_list = self.get_time_segments_totals_trr(dirname)
            print totals_list
            #TODO these should be global variables
            costs_list = self.get_rates_trr(RATES_FOLDER, RATES_FILE)
            print costs_list
            if plan is TRR:
                peak_cost = self.get_time_segment_cost_trr(totals_list[0], \
                                                           costs_list, \
                                                           PEAK_TIME)
                off_peak_cost = self.get_time_segment_cost_trr(totals_list[1], \
                                                               costs_list, \
                                                               OFF_PEAK_TIME)
                night_cost = self.get_time_segment_cost_trr(totals_list[2], \
                                                            costs_list, \
                                                            NIGHT_TIME)
            return peak_cost + off_peak_cost + night_cost

class ResidentialRate(ElectricCNFL):
    def __init__(self):
        pass

    def get_consumption_segment_rr(watts):
        """Determine consumption segment according to watts."""
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

class PreferentialRate(ElectricCNFL):
    def __init__(self):
        pass

    def get_consumption_segment_pr(watts, plan):
        """Determine consumption segment according to watts and plan."""
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
