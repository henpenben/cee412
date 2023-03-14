import streamlit as st
import pandas as pd

'''
# Database Description
The HSIS dataset is a database containing information on traffic accidents that occurred on public highways in the United States. The database includes data on various factors such as driver demographics, accident characteristics, and road conditions, among others. Our database will be a SQL database composed of a fraction of the data available from the HSIS database.
'''



'''
our original dataset had a very large number of columns within its three tables (accident, vehicle, road). Since we were trying to determine crash causes as a result of drivers, and not from the roadways themselves, the road table was not neccessary to include
'''

'''we filtered down the numerous columns to a limited subset, seen below in the ER diagram'''
'''### ER Diagram'''
st.image('er.png')

'''## Limitations of this Dataset
despite being fairly large, this dataset only represents accidents, in washington, in 2002. so it is not the most current. Also, it is not normalized for vehicle miles driven. it only is showing absolute quantities, as that is the data that we have
'''


"# Management"
"first we have to load up the different sheets of our excel file:"
st.code('''
file = './data.xlsx'
accident_source = pd.read_excel(file, sheet_name=0)
vehicle_source = pd.read_excel(file, sheet_name=2)
''')

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


'''we filter out the data tables to the columns we are focusing on (mostly to improve performance and readability)  
example:'''

accCols = ['CASENO', 'ACCTYPE1', 'ACCTYPE2', 'RDSURF']
accident = accident[accCols]
accident = accident.dropna(subset=['ACCTYPE1'])
st.code('''
accCols = ['CASENO', 'ACCTYPE1', 'ACCTYPE2', 'RDSURF']
accident = accident[accCols]
''')

vehCols = ['CASENO', 'VEHNO', 'DRV_AGE', 'DRV_SEX', 'CONTRIB1', 'CONTRIB2', 'MISCACT1', 'MISCACT2', 'VEHTYPE', 'VEHCOND2']
vehicle = vehicle[vehCols]
vehicle = vehicle.dropna(subset=['MISCACT1', 'CONTRIB1'])

"rows of our tables which are missing important / necessary pieces of data are removed"
st.code("accident = accident.dropna(subset=['ACCTYPE1'])")

"we then define dictionaries to map values. some preprocessing on the data was done to determine which of the values were important to keep track of; in this case causes with a count of less than 5 were placed into an 'other' category"
st.code('''
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
''')

"there are lots of other dictionaries, but displaying them all would introduce a lot of clutter"

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


"now that all of our data has been loaded, and the values been mapped in a dictionary, we are ready to join our tables"

'''the vehicle table has a primary key 'CASENO' which is used as a foreign key in the accidents table. the tables are joined in this way.  
example:'''

st.code("combined = pd.merge(accident, vehicle, on='CASENO')")

# join accident and vehicle table on case number
combined = pd.merge(accident, vehicle, on='CASENO')