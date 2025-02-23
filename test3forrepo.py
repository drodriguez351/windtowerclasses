# CLASSES

class Log:
    def __init__(self, time, height, avgMin, avgWindDir, avgWindSpeed, peakWindDir, peakWindSpeed, peakWindDir10, peakWindSpeed10, deviation, temp, tempdiff, dewpoint, relHumidity, baroPressure):
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


# CODE THAT GETS RUN

data = []
with open('2020_10.txt', 'r') as file:
    content = file.readline()  # Read and ignore header
    for line in file:
        values = line.strip().split(',')
        data.append(values)

# Store logs by month
month = Month("October")

# chatGPT code:

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

    log = Log(time, height, avgMin, avgWindDir, avgWindSpeed, peakWindDir, peakWindSpeed, peakWindDir10, peakWindSpeed10, deviation, temp, tempdiff, dewpoint, relHumidity, baroPressure)

    month.addLog(time.split()[0], tower_id, log)  # Group by day

def printTower(tower_to_find):
    # Loop through each day in the stored logs
    
    for day, day_obj in month.days.items():
        # Check if Tower 1000 exists in that day's data
        if tower_to_find in day_obj.towers:
            print(f"Date: {day}, Tower {tower_to_find}")
            
            # Loop through all logs for Tower 1000
            for log in day_obj.towers[tower_to_find].logs:
                print(log)  # Assuming Log has a __str__ method for readable output

def max_temperature_per_day(month, bad_towers):
    max_temps = {}  # Dictionary to store max temperature for each day

    for day, day_obj in month.days.items():  # Loop through each day
        max_temp = float('-inf')  # Initialize with lowest possible value

        for tower in day_obj.towers.values():  # Loop through towers
            if tower.tower in bad_towers:  # Skip bad towers
                continue

            for log in tower.logs:  # Loop through logs
                if log.height == 6 and log.temp >= 10 and log.temp <= 110:  # Check if height is 6 feet
                    max_temp = max(max_temp, log.temp)  # Update max

        # Store the max temperature found for the day
        if max_temp != float('-inf'):  # Ensure we found a valid temperature
            max_temps[day] = max_temp

    return max_temps


def min_temperature_per_day(month, bad_towers):
    min_temps = {}  # Dictionary to store min temperature for each day

    for day, day_obj in month.days.items():  # Loop through each day
        min_temp = float('inf')  # Initialize with highest possible value

        for tower in day_obj.towers.values():  # Loop through towers
            if tower.tower in bad_towers:  # Skip bad towers
                continue
            for log in tower.logs:  # Loop through logs
                if log.height == 6 and log.temp != 0:  # Ignore 0 values
                    min_temp = min(min_temp, log.temp)  # Update min

        # Store the min temperature found for the day if it's valid
        if min_temp != float('inf'):  # Ensure we found a valid temperature
            min_temps[day] = min_temp

    return min_temps

bad_towers = {'\'0300\'','\'0412\'','\'1000\'','\'9404\''}

maxes = max_temperature_per_day(month, bad_towers)
mins = min_temperature_per_day(month, bad_towers)


fileone = open("themaxes.txt", "w")
filetwo = open("themins.txt", "w")

for key in maxes:
    fileone.write(f"{key}: {maxes[key]}\n")

for key in mins:
    filetwo.write(f"{key}: {mins[key]}\n")

# Close the file
fileone.close()
filetwo.close()

def findMaxMonthAvg(height_to_find): 
    day_maxes = []
    for day, day_obj in month.days.items(): 
        day_max = 0
        for tower in day_obj.towers.values():
            for log in tower.logs:
                if(log.height == height_to_find):
                    if (log.temp > day_max and log.temp < 2000.0): 
                        day_max = log.temp
        day_maxes.append(day_max)

    total = 0; 
    for max in day_maxes:
        total += max

    total /= len(day_maxes)
    total = round(total, 2)
    print(f"Max Average: {total}") 
    return total

def findMinMonthAvg(month, bad_towers): 
    mins = min_temperature_per_day(month, bad_towers) 
    total = 0 
    for min in mins.values(): 
        total += min 
    ans = total/len(mins)
    ans = round(ans, 2)
    print(f"Min Average: {ans}")
    return total/len(mins)
    

findMaxMonthAvg(6)
findMinMonthAvg(month, bad_towers)
