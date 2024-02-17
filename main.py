import random
import math

def timeTillLoot(): #predetermines how long to wait for next acolyte to spawn (3-7 minutes)
  max = 7*60;
  min = 3*60;
  return int(random.uniform(min, max));

def rollBuff(): #determines if you received a buff or not, called every 27s. the 1/5 represents the 5 different buffs, since the 6th one (instant reload) can be ignored if no weapons are equipped
  return (random.uniform(0, 1)<=.28) and (random.uniform(0, 1)<=1/5)

def addToArray(startTime): #adds start times to the array and updates the array
  multiStartTimes.append(startTime);
  updateStartTimes()
  if (len(multiStartTimes) > 0):
      numCharms[len(multiStartTimes)-1] += 1 #tracks number of buffs (even if no AC was killed during that time)

def updateStartTimes(): #updates array of buff start times
  if (len(multiStartTimes) > 0): 
    while (i>(multiStartTimes[0]+156)):
      multiStartTimes.pop(0)
      if (len(multiStartTimes) == 0):
        break
        
def calcAvg(x): #number of minutes to receive a 'x' buff (does not include x+1 buffs)
  n = 6-1 #The number of times that a buff could proc before it wears off
  #for [2x, 4x, 8x, 16x, 32x, 64x], use x= [0, 1, 2, 3, 4, 5]
  p = .28 #chance for buff
  t = 27 #time between buff rolls

  value = (1 /  ((math.factorial(n) / (math.factorial(n - x) * math.factorial(x))) * ((p * (1 / n)) ** x) * (1  - (p * ( 1  / n))) ** (n - x))) * (1 / (p * (1 / n)) * t / 60)
  return(value)

print("Calculated results:")
print("Avg mins between any buff:", round((100/5.6 * 27)/60, 2)) #also found on charm's wiki page
print("Avg mins between 2x  buff:", round(calcAvg(0), 2))
print("Avg mins between 4x  buff:", round(calcAvg(1), 2))
print("Avg mins between 8x  buff:", round(calcAvg(2), 2))
print("Avg mins between 16x buff:", round(calcAvg(3), 2))
print("Avg mins between 32x buff:", round(calcAvg(4), 2))
print("Avg mins between 64x buff:", round(calcAvg(5), 2))

#vars
durationHours = 1
durationMins = int(durationHours * 60)
durationSecs = durationMins * 60
numSims = 5000

simTotalBuffs = [0, 0, 0, 0, 0, 0]
simAvgBuffs = [0, 0, 0, 0, 0, 0]
simTotalLoot = 0
simAvgLoot = 0
totalCharms = [0, 0, 0, 0, 0, 0]
avgCharms = [0, 0, 0, 0, 0, 0]
avgTimeBetweenCharms = [0, 0, 0, 0, 0, 0]

for simIndex in range(numSims): #every simulation
  numBuffs = [0, 0, 0, 0, 0, 0] #number of times loot was multiplied
  numCharms = [0, 0, 0, 0, 0, 0] #number of times charm was granted (even if not used)
  rolledTimeTillLoot = timeTillLoot() #predetermined time to wait until next acolyte spawns
  rolledTimeLoot = rolledTimeTillLoot #has be initialized, more information below
  totalLoot = 0 #tracks total loot for the simulation
  multiStartTimes = [] #declare array of all starting times for the buffs
  numAC = 0 #tracks total number of acolytes to spawn
  totalTimeTillLoot = rolledTimeTillLoot/60 #used for calculating average time waited for AC to spawn (true average is 5minutes from (7-3)/2)

  for i in range(durationSecs): #every second 
    if (i == rolledTimeLoot): #adding loot
      updateStartTimes()
      lootMultiplier = 2**len(multiStartTimes) #making buff multiplier. Base SE per is 2 because of the Steel Path +100% loot multiplier. Further double this if you have 2x loot booster
      totalLoot += 1*lootMultiplier #adding loot
      rolledTimeTillLoot = timeTillLoot()#time till next lootroll
      rolledTimeLoot = i + rolledTimeTillLoot #time of next lootroll
        
      #prints for every time an AC dies / you gain loot
      numAC= numAC + 1 #number of acolyte spawns
      rolledTimeTillLootPrint = round(rolledTimeTillLoot/60, 2) 

      if (i != durationSecs): #i can't remember why this condition must be met
        totalTimeTillLoot = totalTimeTillLoot + rolledTimeTillLoot/60

      if (len(multiStartTimes) > 0): #tracks number of single, double, triple, etc. buffs in array
        numBuffs[len(multiStartTimes)-1] += 1 

      #debug prints for each simulation
      """
      print("numBuffs", numBuffs)
      print("Buff start times in seconds:", multiStartTimes)
      print("Loot Multiplier: ", lootMultiplier,"x", sep='')
      print("Total Loot:", totalLoot)
      print("Minutes till next AC:", rolledTimeTillLootPrint)
      print()
      """

    if (i%27 == 0 and i!=0): #every 27s checking if buff received
      rolledBuff = rollBuff();
      if (rolledBuff): #received buff
        addToArray(i); #track start time of buff

    
  #add data from individual simulation to create the main averages
  for a in range(6):
    simTotalBuffs[a] += numBuffs[a]
    simAvgBuffs[a] = round(simTotalBuffs[a]/numSims, 3)
    totalCharms[a] += numCharms[a]
    avgCharms[a] = round(totalCharms[a]/numSims, 3)
    if (avgCharms[a] != 0):
      avgTimeBetweenCharms[a] = round(60/avgCharms[a], 3)
  simTotalLoot += totalLoot
  simAvgLoot = simTotalLoot / numSims
  

  #calc average time between AC
  if (numAC > 0):
    avgTimeTillLoot = round(totalTimeTillLoot / numAC, 3)
  else:
    avgTimeTillLoot = "N/A" #if no AC's killed, this prevents dividing by 0
    
  #individual sim prints for debug, these can be uncommented for smaller simulations, approx numSim < 1000
  """
  print("Sim#:", simIndex+1) 
  print("Number of Acolytes spawned:", numAC)
  print("Average time between AC spawn:", avgTimeTillLoot)
  print("Total loot:", totalLoot)
  print("Number of times loot was multiplied:")
  print("[2x, 4x, 8x, 16x, 32x, 64x]")
  print(numBuffs)
  print("numCharms:", numCharms)
  print("Total charms:", totalCharms)
  print()
  """
  

#end of test prints
print()
print("Test results for ", durationMins, " minutes:", sep='')
print("Number of simulations:", numSims)
print("Format:")
print("[2x, 4x, 8x, 16x, 32x, 64x]")
print("Avg loot:", simAvgLoot)
#print("Total hours spent", numSims * durationHours)
#print("Total charms acquired:")
#print(totalCharms)
print("Average charms acquired:")
print(avgCharms)
print("Average mins between charms:")
print(avgTimeBetweenCharms)
print()
print("Note: For the test, all higher multipliers are still counted as past multipliers.")
print("Example: If you got a 2x buff, then it turned into a 4x buff, the test program still adds 1 to the counter for 2x buff, while the calculated results do not. That is why in the Calculated results section, the time waited for any tier buff is not the same as the time waited for the first tier buff.")
print()
print("To prove that this is the only cause for the deviation between the Calculation and Test numbers, we can compare the average number of charms (any tier) between the program and the calculation by taking into account the deviation. With a high enough sample size, this variable will match fo both methods. See specifics below.")
print()
print("Program's total average charms in", durationMins," minutes.")
print(avgCharms[0], " + ", 
      avgCharms[1], " + ", 
      avgCharms[2], " + ",
      avgCharms[3], " + ", 
      avgCharms[4], " + ", 
      avgCharms[5], " = ",
      avgCharms[0]+avgCharms[1]+avgCharms[2]+avgCharms[3]+avgCharms[4]+avgCharms[5], sep='')
print("Calculated total average charms in", durationMins," minutes.")
print(durationMins, "/8.04 = ", durationMins/8.04, sep='')
