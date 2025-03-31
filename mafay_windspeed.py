import math

# CLASSES

class Log:
    def __init__(self, time, height, avgMin, avgWindDir, avgWindSpeed, peakWindDir, peakWindSpeed, peakWindDir10, peakWindSpeed10, deviation, temp, tempdiff, dewpoint, relHumidity, baroPressure, u, v):
        self.time = time
        self.height = height
        self.avgMin = avgMin
        self.avgWindDir = avgWindDir
        self.avgWindSpeed = avgWindSpeed
        self.peakWindDir = peakWindDir
        self.peakWindSpeed = peakWindSpeed
        self.peakWindDir10 = peakWindDir10
        self.peakWindSpeed10 = peakWindSpeed10
        self.deviation = deviation
        self.temp = temp
        self.tempdiff = tempdiff
        self.dewpoint = dewpoint
        self.relHumidity = relHumidity
        self.baroPressure = baroPressure
        self.u = u
        self.v = v

    def __str__(self):  # Fixed __str__ method
        return (f'Time: {self.time}, Height: {self.height}, Average Minute: {self.avgMin}, '
                f'Average Wind Direction: {self.avgWindDir}, Average Wind Speed: {self.avgWindSpeed}, '
                f'Peak Wind Direction: {self.peakWindDir}, Peak Wind Speed: {self.peakWindSpeed}, '
                f'Peak Wind Direction 10 Minute: {self.peakWindDir10}, Peak Wind Speed 10 Minute: {self.peakWindSpeed10}, '
                f'Deviation: {self.deviation}, Temperature: {self.temp}, Temperature Difference: {self.tempdiff}, '
                f'Dewpoint: {self.dewpoint}, Relative Humidity: {self.relHumidity}, Barometric Pressure: {self.baroPressure}')


class Tower:
    def __init__(self, tower):
        self.tower = tower
        self.logs = []  # Fixed instance variable

    def addLog(self, log):
        self.logs.append(log)


class Day:
    def __init__(self, day):
        self.day = day
        self.towers = {}  # Store towers by ID

    def addLog(self, tower_id, log):
        if tower_id not in self.towers:
            self.towers[tower_id] = Tower(tower_id)
        self.towers[tower_id].addLog(log)



class Month:
    def __init__(self, month):
        self.month = month
        self.days = {}  # Store days by date

    def addLog(self, date, tower_id, log):
        if date not in self.days:
            self.days[date] = Day(date)
        self.days[date].addLog(tower_id, log)

def get_all_towers(monthobj):
    towerlist = []
    for day_obj in monthobj.days.values():  # Loop through all days
        for tower_obj in day_obj.towers.values():
            if tower_obj.tower not in towerlist:
                towerlist.append(tower_obj.tower)
    return towerlist


# CODE THAT GETS RUN

data = []
filefound = False
while True:
    try:
        filename = input("File: ")
        with open(filename + ".txt", 'r') as file:
            content = file.readline()  # Read and ignore header
            for line in file:
                values = line.strip().split(',')
                data.append(values)
        filefound = True
    except:
        print("File does not exist in this directory. Please try again.")
        continue
    if (filefound):
        break

# Store logs by month
month = Month("October")

# ACCESSING DATA
for line in data:
    time = line[0]
    tower_id = line[1].strip('"')  # Remove quotes
    height = int(line[2].strip('"'))
    avgMin = int(line[3].strip('"'))
    avgWindDir = line[4].strip('"')
    avgWindSpeed = int(line[5].strip('"')) if line[5].strip('"') else 0
    peakWindDir = int(line[6].strip('"')) if line[6].strip('"') else 0
    peakWindSpeed = int(line[7].strip('"')) if line[7].strip('"') else 0
    peakWindDir10 = int(line[8].strip('"')) if line[8].strip('"') else 0
    peakWindSpeed10 = int(line[9].strip('"')) if line[9].strip('"') else 0
    deviation = int(line[10].strip('"')) if line[10].strip('"') else 0
    temp = float(line[11].strip('"')) if line[11].strip('"') else 0
    tempdiff = float(line[12].strip('"')) if line[12].strip('"') else 0
    dewpoint = float(line[13].strip('"')) if line[13].strip('"') else 0
    relHumidity = int(line[14].strip('"')) if line[14].strip('"') else 0
    baroPressure = line[15].strip('"') if line[15].strip('"') else 0
    if avgWindDir != '':
        u = -abs(avgWindSpeed) * math.sin(math.radians(float(avgWindDir)))
        v = -abs(avgWindSpeed) * math.cos(math.radians(float(avgWindDir)))
    else:
        u = 'A'
        v = 'A'

    log = Log(time, height, avgMin, avgWindDir, avgWindSpeed, peakWindDir, peakWindSpeed, peakWindDir10, peakWindSpeed10, deviation, temp, tempdiff, dewpoint, relHumidity, baroPressure, u, v)

    month.addLog(time.split()[0], tower_id, log)  # Group by day

# BAD TOWER DATA COLLECTION

allTowers = get_all_towers(month)



def windspeedaverage(month, comp):
    comps = []  # Dictionary to store min temperature for each day

    for day, day_obj in month.days.items():  

        for tower in day_obj.towers.values():  
            for log in tower.logs: 
                if log.height == 54 and log.u != 'A' and log.v != 'A':  
                    if comp == "u":
                        comps.append(log.u)
                    else:
                        comps.append(log.v)
    sum = 0
    for val in comps:
        sum += val
    return round(sum / len(comps), 2)

# LEFT OFF HERE :)

def windbuckets(month):
    buckets = {'N': 0, 'NE': 0, 'E': 0, 'SE': 0, 'S': 0, 'SW': 0, 'W': 0, 'NW': 0}

    for day, day_obj in month.days.items():  
        for tower in day_obj.towers.values():  
            for log in tower.logs: 
                if log.height == 54 and log.u != 'A' and log.v != 'A':
                    dir = float(log.avgWindDir)
                    if dir >= 337.5 or dir < 22.5:
                        buckets['N'] += 1
                    elif dir >= 22.5 and dir < 67.5:
                        buckets['NE'] += 1
                    elif dir >= 67.5 and dir < 112.5:
                        buckets['E'] += 1
                    elif dir >= 112.5 and dir < 157.5:
                        buckets['SE'] += 1
                    elif dir >= 157.5 and dir < 202.5:
                        buckets['S'] += 1
                    elif dir >= 202.5 and dir < 247.5:
                        buckets['SW'] += 1
                    elif dir >= 247.5 and dir < 292.5:
                        buckets['W'] += 1
                    else:
                        buckets['NW'] += 1

    return buckets

                    
                


def maxwindspeed(month):
    speeds = []  # Dictionary to store min temperature for each day

    for day, day_obj in month.days.items():  

        for tower in day_obj.towers.values():  
            for log in tower.logs: 
                if log.height == 54 and log.u != 'A' and log.v != 'A':  
                    speeds.append(log.avgWindSpeed)
    return round(max(speeds), 2)
        



fileone = open(filename + "_ws.txt", "w")
    
ws_avg_u = windspeedaverage(month, "u")
ws_avg_v = windspeedaverage(month, "v")

avg_ws = round(math.sqrt(math.pow(ws_avg_u, 2) + math.pow(ws_avg_v, 2)), 2)
max_ws = maxwindspeed(month)

wind_buckets = windbuckets(month)

print(wind_buckets)

freq_wind = max(wind_buckets, key=wind_buckets.get)
print(freq_wind)



fileone.write(f"{max_ws},{avg_ws},{freq_wind}\n")

# Close the file
fileone.close()



