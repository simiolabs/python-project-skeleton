import time
#CNFL

OFF_PEAK_TIME =         0
PEAK_TIME =             1
NIGHT_TIME =            2

#times
start_offpeak_time1 = time.strptime('06:01', '%H:%M')
end_offpeak_time1   = time.strptime('10:00', '%H:%M')
start_peak_time1    = time.strptime('10:01', '%H:%M')
end_peak_time1      = time.strptime('12:30', '%H:%M')
start_offpeak_time2 = time.strptime('12:31', '%H:%M')
end_offpeak_time2   = time.strptime('17:30', '%H:%M')
start_peak_time2    = time.strptime('17:31', '%H:%M')
end_peak_time2      = time.strptime('20:00', '%H:%M')
start_night_time1   = time.strptime('20:01', '%H:%M')
end_night_time1     = time.strptime('23:59', '%H:%M')
start_night_time2   = time.strptime('00:00', '%H:%M')
end_night_time2     = time.strptime('06:00', '%H:%M')

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


#determine segment according to time
def get_time_segment(timestamp):
    ts = time.strptime(timestamp, '%H:%M')
    #peak time
    if ((ts >= start_peak_time1 and ts <= end_peak_time1) or
        (ts >= start_peak_time2 and ts <= end_peak_time2)):
        return PEAK_TIME
    #offpeak time
    elif ((ts >= start_offpeak_time1 and ts <= end_offpeak_time1) or
          (ts >= start_offpeak_time2 and ts <= end_offpeak_time2)):
        return OFF_PEAK_TIME
    #night time
    elif ((ts >= start_night_time1 and ts <= end_night_time1) or
         (ts >= start_night_time2 and ts <= end_night_time2)):
        return NIGHT_TIME
    else:
        return -1

#determine segment according to plan
#time residential rate
def get_consumption_segment_trr(watts):
    if (watts <= TRR_LOW_POWER):
        return TRR_LOW
    elif (watts > TRR_LOW_POWER and watts <= TRR_HIGH_POWER):
        return TRR_MID
    elif (watts > TRR_HIGH_POWER):
        return TRR_HIGH
    else:
        return -1

#residential rate
def get_consumption_segment_tr(watts):
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

#preferential rate
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

#fire department tribute
def get_fire_department_tribute(total_watts, total_cost, plan):
    if (plan == 'TRR' or plan == 'RR' or plan == 'PR'):
        return (total_cost * FIRE_DEP_TRIBUTE)
    else:
        return (total_cost / total_watts * FIRE_DEP_TAX * FIRE_DEP_TRIBUTE)

#street lighting tribute
def get_street_lighting_tribute(total_watts):
    return (total_watts * STREET_LIGHT_TRIBUTE)
