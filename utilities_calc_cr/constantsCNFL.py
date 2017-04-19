#CNFL

OFF_PEAK_TIME =         0
PEAK_TIME =             1
NIGHT_TIME =            2

START_OFF_PEAK_TIME1 =  0601
END_OFF_PEAK_TIME1 =    1000
START_PEAK_TIME1 =      1001
END_PEAK_TIME1 =        1230
START_OFF_PEAK_TIME2 =  1231
END_OFF_PEAK_TIME2 =    1730
START_PEAK_TIME2 =      1731
END_PEAK_TIME2 =        2000
START_NIGHT_TIME =      2001
END_NIGHT_TIME =        6000

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
def timeSegment(ts):
    #offpeak time
    if ((ts >= START_OFF_PEAK_TIME1 and ts <= END_OFF_PEAK_TIME1) or
        (ts >= START_OFF_PEAK_TIME2 and ts <= END_OFF_PEAK_TIME2)):
        return OFF_PEAK_TIME
    #peak time
    elif ((ts >= START_PEAK_TIME1 and ts <= END_PEAK_TIME1) or
          (ts >= START_PEAK_TIME2 and ts <= END_PEAK_TIME2)):
        return PEAK_TIME
    #night time
    elif (ts >= START_NIGHT_TIME and ts <= END_NIGHT_TIME):
        return NIGHT_TIME
    else:
        return EXIT_FAILURE

#determine segment according to plan
#time residential rate
def get_consumption_segment_trr(watts):
    if (totalWatts <= TRR_LOW_POWER):
        return TRR_LOW
    elif (totalWatts > TRR_LOW_POWER and totalWatts <= TRR_HIGH_POWER):
        return TRR_MID
    elif (totalWatts > TRR_HIGH_POWER):
        return TRR_HIGH
    else:
        return EXIT_FAILURE

#time residential
def get_consumption_segment_tr(watts):
    if (totalWatts <= RR_FIXED_CHARGE):
        return RR_FIXED
    elif (totalWatts > RR_FIXED_CHARGE and totalWatts <= RR_LOW_POWER):
        return RR_LOW
    elif (totalWatts > RR_LOW_POWER and totalWatts <= RR_HIGH_POWER):
        return RR_MID
    elif (totalWatts > RR_HIGH_POWER):
        return RR_HIGH
    else:
        return EXIT_FAILURE

#preferential rate
def consumption_segment_pr(watts, plan):
    if (totalWatts <= PR_LOW_POWER and plan == PR_ENERGY):
        return PR_E_LOW
    elif (totalWatts <= PR_LOW_POWER and plan == PR_POWER):
        return PR_P_LOW
    elif (totalWatts > PR_LOW_POWER and totalWatts <= PR_MID_POWER):
        return PR_MID
    elif (totalWatts > PR_MID_POWER and totalWatts <= PR_HIGH_POWER):
        return PR_MID
    elif (totalWatts > PR_HIGH_POWER and plan == PR_ENERGY):
        return PR_E_HIGH
    elif (totalWatts > PR_HIGH_POWER and plan == PR_POWER):
        return PR_P_HIGH
    else:
        return EXIT_FAILURE

#fire department tribute
def get_fire_department_tribute(total_watts, total_cost, plan):
    if (plan == TRR or plan == RR or plan == PR):
        return (totalCost * FIRE_DEP_TRIBUTE)
    else:
        return (totalCost / totalWatts * FIRE_DEP_TAX * FIRE_DEP_TRIBUTE)

#street lighting tribute
def get_street_lighting_tribute(totalWatts):
    return (totalWatts * STREET_LIGHT_TRIBUTE)
