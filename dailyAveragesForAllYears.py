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
    
    def numDays(self):
        return len(self.days)

class Year: 
    def __init__(self, year):
        self.year = year
        self.months = {}  # Store months by num

    def addLog(self, month, date, tower_id, log):
        if month not in self.months:
            self.months[month] = Month(month); 
        self.months[month].addLog(date, tower_id, log)

def get_all_towers(monthlist):
    towerlist = []
    for monthobj in monthlist:
        for day_obj in monthobj.days.values():  # Loop through all days
            for tower_obj in day_obj.towers.values():
                if tower_obj.tower not in towerlist:
                    towerlist.append(tower_obj.tower)
    return towerlist


# CODE THAT GETS RUN


filefound = False
viable = []
for i in range(1,10):
    viable.append("0" + str(i))
    viable.append(str(i))
viable += ["10","11","12"]

while True:
    monthInput = input("Month: ")
    if monthInput in viable:
        break
    else:
        print("Really? You think that we have a month of " + monthInput + "?? Nuh-uh. Try again buddy. - David")
        continue

viabletwo = []
for i in range(2012,2021):
    viabletwo.append(str(i))

while True:
    startYear = input("Start Year: ")
    if startYear in viabletwo:
        startYear = int(startYear[2:])
        break
    else:
        print("Really? You think that we have a year of " + startYear + "?? Nuh-uh. Try again buddy. - David")
        continue

while True:
    endYear = input("End Year: ")
    if endYear in viabletwo:
        endYear = int(endYear[2:])
        break
    else:
        print("Really? You think that we have a year of " + endYear + "?? Nuh-uh. Try again buddy. - David")
        continue


m = ""
if (monthInput == "01" or monthInput == "1"):
    m = "January"
elif (monthInput == "02" or monthInput == "2"):
    m = "February"
elif (monthInput == "03" or monthInput == "3"):
    m = "March"
elif (monthInput == "04" or monthInput == "4"):
    m = "April"
elif (monthInput == "05" or monthInput == "5"):
    m = "May"
elif (monthInput == "06" or monthInput == "6"):
    m = "June"
elif (monthInput == "07" or monthInput == "7"):
    m = "July"
elif (monthInput == "08" or monthInput == "8"):
    m = "August"
elif (monthInput == "09" or monthInput == "9"):
    m = "September"
elif (monthInput == "10"):
    m = "October"
elif (monthInput == "11"):
    m = "November"
elif (monthInput == "12"):
    m = "December"

m += "_daily"

if len(monthInput) == 1:
    monthInput = "0" + monthInput


monthlist = []
for i in range(startYear,endYear + 1):
    data = []
    month = Month("20" + str(i)) 
    filename = "20" + str(i) + "_" + monthInput
    with open(filename + ".txt", 'r') as file:
        content = file.readline()  # Read and ignore header
        for line in file:
            values = line.strip().split(',')
            data.append(values)

    # Store logs by year


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

        log = Log(time, height, avgMin, avgWindDir, avgWindSpeed, peakWindDir, peakWindSpeed, peakWindDir10, peakWindSpeed10, deviation, temp, tempdiff, dewpoint, relHumidity, baroPressure)

        month.addLog(time.split()[0], tower_id, log)  # Group by day

    monthsize = month.numDays()
    monthlist.append(month)

# BAD TOWER DATA COLLECTION

allTowers = get_all_towers(monthlist)
newlist = []


# OUTLIER ANALYSIS

def errorCheck1(monthlist):
    towerlist = []
    for monthobj in monthlist:
        for day_obj in monthobj.days.values():
            for tower_obj in day_obj.towers.values():
                for log_obj in tower_obj.logs:
                    if (log_obj.temp < 10 or log_obj.temp > 110) and (tower_obj.tower not in towerlist) and (log_obj.temp != 0) and (log_obj.height == 6):
                        towerlist.append(tower_obj.tower)
    return towerlist

def errorCheck2(monthlist, badSoFar):

    towerlist = []

    for elem in badSoFar:
        towerlist.append(elem)
    
    for monthobj in monthlist:
        while True:
            allTemps = []
            found = False

            for day_obj in monthobj.days.values():
                for tower_obj in day_obj.towers.values():
                    if (tower_obj.tower not in towerlist):
                        for log_obj in tower_obj.logs:
                            if log_obj.height == 6 and log_obj.temp != 0:
                                allTemps.append(log_obj.temp)
            
            firstMin = min(allTemps)
            print(firstMin)

            for day_obj in monthobj.days.values():
                for tower_obj in day_obj.towers.values():
                    if (tower_obj.tower not in towerlist):
                        for log_obj in tower_obj.logs:
                            if log_obj.height == 6:
                                if (log_obj.temp == firstMin):
                                    curTower = tower_obj.tower
                                    print(curTower)
                                    curDate = day_obj
                                    found = True
                            if (found):
                                break
                    if (found):
                        break
                if (found):
                    break
            
            allNewTemps = []

            for tower_obj in curDate.towers.values():
                if (tower_obj.tower not in towerlist) and (tower_obj.tower != curTower):
                    for log_obj in tower_obj.logs:
                        if (log_obj.height == 6) and (log_obj.temp != 0):
                            allNewTemps.append(log_obj.temp)
                
            newMin = min(allNewTemps)
            print(newMin)

            if (newMin - firstMin >= 10):
                towerlist.append(curTower)
            else:
                break

        while True:
            allTemps = []
            found = False

            for day_obj in monthobj.days.values():
                for tower_obj in day_obj.towers.values():
                    if (tower_obj.tower not in towerlist):
                        for log_obj in tower_obj.logs:
                            if log_obj.height == 6 and log_obj.temp != 0:
                                allTemps.append(log_obj.temp)
            
            firstMax = max(allTemps)
            print(firstMax)

            for day_obj in monthobj.days.values():
                for tower_obj in day_obj.towers.values():
                    if (tower_obj.tower not in towerlist):
                        for log_obj in tower_obj.logs:
                            if log_obj.height == 6:
                                if (log_obj.temp == firstMax):
                                    curTower = tower_obj.tower
                                    print(curTower)
                                    curDate = day_obj
                                    found = True
                            if (found):
                                break
                    if (found):
                        break
                if (found):
                    break
            
            allNewTemps = []

            for tower_obj in curDate.towers.values():
                if (tower_obj.tower not in towerlist) and (tower_obj.tower != curTower):
                    for log_obj in tower_obj.logs:
                        if (log_obj.height == 6) and (log_obj.temp != 0):
                            allNewTemps.append(log_obj.temp)
                
            newMax = max(allNewTemps)
            print(newMax)

            if (firstMax - newMax >= 10):
                towerlist.append(curTower)
            else:
                break
    
    return towerlist
    

ec1 = errorCheck1(monthlist)
newlist = errorCheck2(monthlist, ec1)

def printTower(tower_to_find):
    
    for day, day_obj in month.days.items():
        
        if tower_to_find in day_obj.towers:
            print(f"Date: {day}, Tower {tower_to_find}")
            
            for log in day_obj.towers[tower_to_find].logs:
                print(log)  

def max_temperature_per_day(monthlist, bad_towers):
    max_temp_list = []

    for month in monthlist:
        max_temps = {}
        for day, day_obj in month.days.items():  # Loop through each day
            max_temp = float('-inf') 

            for tower in day_obj.towers.values():  # Loop through towers
                if tower.tower in bad_towers:  # Skip bad towers
                    continue

                for log in tower.logs:  # Loop through logs
                    if log.height == 6 and log.temp >= 10 and log.temp <= 110:  # Check if height is 6 feet
                        max_temp = max(max_temp, log.temp)  # Update max

                justDay = day[3:5]
            
            if max_temp != float('inf'):  
                max_temps[justDay] = max_temp
        max_temp_list.append(max_temps)

    return max_temp_list


def min_temperature_per_day(monthlist, bad_towers):
    min_temp_list = []

    for month in monthlist:
        min_temps = {}
        for day, day_obj in month.days.items():  
            min_temp = float('inf')  

            for tower in day_obj.towers.values():  
                if tower.tower in bad_towers:  # Skip bad towers
                    continue
                for log in tower.logs: 
                    if log.height == 6 and log.temp != 0:  
                        min_temp = min(min_temp, log.temp)  

            justDay = day[3:5]
            
            if min_temp != float('inf'):  
                min_temps[justDay] = min_temp
        min_temp_list.append(min_temps)

    return min_temp_list



maxes = max_temperature_per_day(monthlist, newlist)
mins = min_temperature_per_day(monthlist, newlist)
allDays = maxes[0].keys()

fileone = open(m + "_allyears.txt", "w")

for day in allDays:
    day_data = []
    for month_dict in maxes:
        day_data.append(month_dict[day])
    day_max = max(day_data)

    total = 0
    for i in day_data:
        total += i
    
    day_avg_max = round(total/len(day_data), 2)

    day_data = []
    for month_dict in mins:
        day_data.append(month_dict[day])
    day_min = min(day_data)

    total = 0
    for i in day_data:
        total += i
    
    day_avg_min = round(total/len(day_data), 2)

    fileone.write(f"{day_max} {day_min} {day_avg_max} {day_avg_min}\n")





# Close the file
fileone.close()




