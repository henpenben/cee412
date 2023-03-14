import streamlit as st
import pandas as pd
import math





file = './data.xlsx'

#Have seperate tables - one for accidents, roads, and vehicles
@st.cache_data
def loadAcc():
    return pd.read_excel(file, sheet_name=0)
@st.cache_data
def loadVeh():
    return pd.read_excel(file, sheet_name=2)

accident_source = loadAcc()
vehicle_source = loadVeh()

accident = accident_source
vehicle = vehicle_source


accCols = ['CASENO', 'ACCTYPE1', 'RDSURF']
accident = accident[accCols]
accident = accident.dropna(subset=['ACCTYPE1'])


vehCols = ['CASENO', 'DRV_AGE', 'CONTRIB1', 'MISCACT1']
vehicle = vehicle[vehCols]
vehicle = vehicle.dropna(subset=['DRV_AGE', 'MISCACT1', 'CONTRIB1'])



# ACCTYPE1/ACCTYPE2 dictionary
acctypeDict = {
    '1' : ('VEH TRN RIGHT'      ,'Vehicle turning right'),
    '2' : ('VEH TRN LEFT'       ,'Vehicle turning left'),
    '3' : ('VEH BACKING'        ,'Vehicle backing'),
    '4' : ('ALL OTHERS'         ,'All others'),
    '5' : ('NOT STATED'         ,'Not stated'),
    '10' : ('ENTERN AT ANGLE'   ,'Entering at angle'),
    '11' : ('SD/MV-SIDESWIPE'   ,'Same direction/both straight/both moving/sideswipe'),
    '12' : ('SD/STP-SIDESWIPE'  ,'Same direction/both straight/one stopped/sideswipe'),
    '13' : ('SD/MV-REAR END'    ,'Same direction/both straight/both moving/rear end'),
    '14' : ('SD/STP-REAR END'   ,'Same direction/both straight/one stopped/rear end'),
    '15' : ('SD/LFT-STRAIGHT'   ,'Same direction/one left turn/one straight'),
    '16' : ('SD/RGH/STRAIGHT'   ,'Same direction/one right turn/one straight'),
    '71' : ('SD/RGH-MV/SDSWIP'  ,'Same direction/both turning right/both moving/sideswipe'),
    '72' : ('SD/RGH-STP/SDSWP'  ,'Same direction/both turning right/one stopped/sideswipe'),
    '73' : ('SD/RGH-MV/R-END'   ,'Same direction/both turning right/both moving/rear end'),
    '74' : ('SD/RGH/STP/R-END'  ,'Same direction/both turning right/one stopped/rear end'),
    '81' : ('SD/LFT-MV/SDSWP'   ,'Same direction/both turning left/both moving/sideswipe'),
    '82' : ('SD/LFT-STP/SDSWP'  ,'Same direction/both turning left/one stopped/sideswipe'),
    '83' : ('SD/LFT-MV/R-END'   ,'Same direction/both turning left/both moving/rear end'),
    '84' : ('SD/LFT/STP/R-END'  ,'Same direction/both turning left/one stopped/rear end'),
    '19' : ('ONE ENTR PRK POS'  ,'One entering parked position'),
    '20' : ('ONE LEV PRK POS'   ,'One leaving parked position'),
    '21' : ('ONE ENTR DRVWAY'   ,'One entering driveway'),
    '22' : ('ONE LEV DRVWAY'    ,'One leaving driveway'),
    '23' : ('SAME DIR-ALL OTH'  ,'Same direction/all others'),
    '24' : ('OD/MV-HEAD ON'     ,'Opposite direction/both moving/head on'),
    '25' : ('OD/STP-HEAD ON'    ,'Opposite direction/one stopped/head on'),
    '26' : ('OD/MV-/SDSWIP'     ,'Opposite direction/both straight/both moving/sideswipe'),
    '27' : ('OD/STP/SDSWIP'     ,'Opposite direction/both straight/one stopped/sideswipe'),
    '28' : ('OD/LFT-STRAIGHT'   ,'Opposite direction/one left turn/one straight'),
    '29' : ('OD/LFT RGHT-TURN'  ,'Opposite direction/one left turn/one right turn'),
    '30' : ('OPPOS DIR ALL OTH' ,'Opposite direction/all others'),
    '32' : ('COLL PARKED VEH'   ,'One parked/one moving'),
    '40' : ('TRAIN STRK MV VEH' ,'Train struck moving vehicle'),
    '41' : ('TRAIN STRK STP VEH','Train struck stalled or stopped veh'),
    '42' : ('VEH STRK MV TRAIN' ,'Vehicle struck moving train'),
    '43' : ('VEH STRK STP TRAIN','Vehicle struck stopped train'),
    '44' : ('COLL W/UNICYCLE'   ,'Unicycle'),
    '45' : ('COLL W/BICYCLE'    ,'Bicycle'),
    '46' : ('COLL W/TRICYCLE'   ,'Tricycle'),
    '47' : ('DA,HRSE,COW,ETC'   ,'Domestic animal(horse, cow, sheep, etc)'),
    '48' : ('DA-OTH,CAT,DOG'    ,'Domestic animal other (cat, dog, etc)'),
    '49' : ('NDA-DEER,BEAR,ELK' ,'Non-domestic animal (deer, bear, elk, etc)'),
    '50' : ('COLL-FIXED OBJECT' ,'Fixed object'),
    '51' : ('COLL-OTHER OBJECT' ,'Other object'),
    '52' : ('VEH OVERTURNED'    ,'Vehicle overturned'),
    '53' : ('FELL/JMP/PUSH VH'  ,'Fell, jumped, or pushed from vehicle'),
    '54' : ('FIRE STRT IN VEH'  ,'Fire started in vehicle'),
    '55' : ('CARBON MONOXIDE'   ,'Accidentally overcome by carbon monoxide poisoning'),
    '56' : ('BRK PART VEH INJ'  ,'Breakage of any part of vehicle resulting in injury or property damage'),
    '57' : ('ALL OTHR NON-COLL' ,'All other non-collision')
}

# RDSURF Road surface dictionary
rdsurfDict = {
    '0' : ('NOT STATED',"Unknown"),
    '1' : ('DRY',"Dry roadway"),
    '2' : ('WET' ,"Wet roadway"),
    '3' : ('SNOW',"Snowy roadway"),
    '4' : ('ICE',"Icy roadway")
}

# MISCACT Dictionary for entries with a count of at least 5 in the dataset
miscactDict = {
    '3': ('OTHER SKIDDING', 'Other skidding'),
    '5': ('AVOID OTH VEH', 'Avoiding another vehicle'),
    '14': ('SLOWN FOR O/VEH', 'Slowing for another vehicle'),
    '19': ('STPD FOR/AT SGN', 'Stopped for or at signal or sign'),
    '20': ('STPD FOR PED', 'Stopped for pedestrian'),
    '21': ('STPD FOR OTH VEH', 'Stopped for another vehicle'),
    '25': ('STPD IN TRAFF', 'Stopped in line of traffic'),
    '27': ('STPD TO TURN RIGHT', 'Stopped prior to turning right'),
    '28': ('STPD TO TURN LEFT ', 'Stopped prior to turning left'),
    '29': ('STPD PROC TRNING', 'Stopped in process of turning'),
    '57': ('TRAILER OVERTRN', 'Trailer overturned'),
    '87': ('CONSTR AREA', 'Construction area'),
    '92': ('VIEW OBSCURED VEH', 'View obscured by other vehicle'),
    '96': ('STOLEN VEH INVOL', 'Stolen vehicle involved'),
    '97': ('HIT & RUN', 'Hit & run'),
    '98': ('VIEW OBSCURED', 'View obscured by frost, ice, etc. on windshield')
}

# CONTRIB Dictionary for entries with a count of at least 5 in the dataset
contribDict = {
    '2': ('INFLUENCE OF DRUGS', 'Under influence of drugs'),
    '3': ('EXCD SPEED LIMIT', 'Exceeded stated speed limit'),
    '4': ('EXCD SAFE SPEED', 'Exceeded reasonably safe speed'),
    '5': ('RIGHT OF WAY', 'Did not grant right-of-way to veh'),
    '6': ('IMPROPER PASSING', 'Improper passing'),
    '7': ('FOLLOWING TOO CLOSE', 'Following too closely'),
    '8': ('OVER CENTERLINE', 'Over centerline'),
    '9': ('FAILING TO SIGNAL', 'Failing to signal'),
    '10': ('IMPROPER TURNING', 'Improper turning'),
    '11': ('FAIL STP&GO LGHT', 'Disregarded stop & go light'),
    '12': ('FAIL STP SGN/LGHT', 'Disregarded sto sign or red flashing light'),
    '14': ('FAIL ASLEEP', 'Apparently asleep'),
    '15': ('IMP PRK LOCATION', 'Improper parking location'),
    '16': ('OPER DEF EQPMNT', 'Operating defective equipment'),
    '17': ('OTHER', 'Other'),
    '20': ('IMPROPER U-TURN', 'Improper U-turn'),
    '21': ('NO HEADLIGHT', 'Headlight violation (no lights or failed to dim)'),
    '22': ('ROW TO PED/CYC', 'Did not grant right of way to pedestrian/pedalcyclist, etc.'),
    '23': ('INATTENTION', 'Inattention'),
}




# join accident and vehicle table on case number
combined = pd.merge(accident, vehicle, on='CASENO')
"# Cleaning Up"

"the tables were joined on the key constraint described earlier (CASENO)"
st.code("combined = pd.merge(accident, vehicle, on='CASENO')")

combined

"Note that ACCTYPE2 & CONTRIB2 are secondary reasons. Displayed reasons in the charts below will be the primary reasons only."

"below you will find all the columns available. of these, RDSURF, ACCTYPE1/2, CONTRIB1/2, MISCACT1/2 all have code values that can be decoded with the dictionaries"
combined.columns

"decoding these values by hand is a bit clunky and doesn't make for pretty charts, so lets make a mapping function to handle that"
"here's an example for ACCTYPE1"
st.code('''
# adds a row for the accident type called 'Accident Type'
def accTypeNamer(row):
    #Grab the current row's coded value
    key = row['ACCTYPE1']
    #They are stored as floats, but encoded in the dictionary as whole-number strings
    #(these aren't integers because there is the occasional alphanumeric code)
    key = str(round(key))
    #if our decoding dictionary doesn't have it, put it under "Other"
    if(not acctypeDict.get(key)):
        row['Accident Type'] = "Other"
        return row
    #Get the decoded name from the dictionary
    name = acctypeDict.get(key)[1]
    row['Accident Type'] = name
    return row
''')


st.code('''
# add the named accident types
t1 = combined.apply(accTypeNamer, axis=1)
''')

"Similar processing is done for other fields."
"Ages are grouped into age groups; 0-15, 16-19, 19-21, 22-30, 31-65, and 65+"

def accTypeNamer(row):
    key = row['ACCTYPE1']
    key = str(round(key))
    if(not acctypeDict.get(key)):
        row['Accident Type'] = "Other"
        return row
    name = acctypeDict.get(key)[1]
    row['Accident Type'] = name
    return row

def ageGrouper(row):
    key = row['DRV_AGE']
    key = round(key)

    if key < 16:
        age_group = "0-15"
    elif key < 20:
        age_group = "16-19"
    elif key < 22:
        age_group = "19-21"
    elif key < 31:
        age_group = "22-30"
    elif key < 66:
        age_group = "31-65"
    else:
        age_group = "65+"

    row["Age Group"] = age_group
    return row

def contribNamer(row):
    key = row['CONTRIB1']
    key = str(round(key))
    if(not contribDict.get(key)):
        row['Contributing Factor'] = "Other"
        return row
    name = contribDict.get(key)[1]
    row['Contributing Factor'] = name
    return row

def miscactNamer(row):
    key = row['MISCACT1']
    key = str(round(key))
    if(not miscactDict.get(key)):
        row['Misc Factor'] = "Other"
        return row
    name = miscactDict.get(key)[1]
    row['Misc Factor'] = name
    return row

def rdsurfNamer(row):
    key = row['RDSURF']
    # invalid values were not filtered earlier
    if(math.isnan(key)):
        key = -1
    key = str(round(key))
    if(not rdsurfDict.get(key)):
        row['Roadway Condition'] = "Other"
        return row
    name = rdsurfDict.get(key)[1]
    row['Roadway Condition'] = name
    return row


"a group favorite is MISCACT1 == A5, which corresponds to an accident that was the result of lava on the roadway"
@st.cache_data
def nameCols():
    t1 = combined.apply(accTypeNamer, axis=1)
    t2 = t1.apply(ageGrouper, axis=1)
    t3 = t2.apply(contribNamer, axis=1)
    t4 = t3.apply(miscactNamer, axis=1)
    t5 = t4.apply(rdsurfNamer, axis=1)
    return t5
named = nameCols()[['Accident Type', 'Age Group', 'Contributing Factor', 'Misc Factor', 'Roadway Condition']]
named
"much better"
import matplotlib.pyplot as plt

"# Analysis"
"### how many accidents done in each age group?"


"group by age, then by accident type"
st.code('''# group by age
grouped = named.groupby(['Age Group', 'Accident Type']).size().reset_index(name='count')''')


grouped = named.groupby(['Age Group', 'Accident Type']).size().reset_index(name='count')

fig, ax = plt.subplots()
ax.hist(grouped['Age Group'], bins = 6)
st.pyplot(fig)



"### Maybe you want to make your own charts?"
chosen_X = st.selectbox("pick your first group", named.columns)
wants_G = st.checkbox("group by second element?")
chosen_G = False


if(wants_G):
    chosen_G = st.selectbox("group by....", named.columns.drop(chosen_X))

if(chosen_G):
    grouped = named.groupby([chosen_X, chosen_G]).size().reset_index(name='count').set_index(chosen_X)
else:
    grouped = named.groupby([chosen_X]).size().reset_index(name='count').set_index(chosen_X)
    st.bar_chart(grouped)

# num_bins = st.slider("how many bins?", 1, 100, 6, 1)

grouped


# fig, ax = plt.subplots()
# plt.figure()

# # grouped.plot(legend=True)
# # plt.legend(loc='best')
# # ax.hist(grouped[chosen_X], bins = num_bins)
# # lines, labels = ax.get_legend_handles_labels()
# # ax.legend(loc='best')
# # st.pyplot(fig)