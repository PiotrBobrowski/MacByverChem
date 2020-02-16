import csv

# read the file to buffer
with open('6.csv', newline = '') as csvDataFile:
    csvData = list(csv.reader(csvDataFile))
# end reading the file to buffer

# find position of important data in buffer
for row in range(len(csvData)):
    for col in range(len(csvData[row])):

        if 'kV:' in csvData[row][col]:
            AccVol = csvData[row][col].replace('kV:','')

        if 'AmpT:' in csvData[row][col]:
            AmpT = csvData[row][col].replace(' AmpT:','')

        if 'Lsec :' in csvData[row][col]:
            Lsec = csvData[row][col].replace(' Lsec :','')

        if 'Wt %' in csvData[row][col]:
            ReadBegin = row

        if 'Total' in csvData[row][col]:
            ReadEnd = row

del row, col
# end finding position of imortant data in buffer

# copy the important data to lists
Elements = []
WeightC = []
AtomicC = []
for row in range(ReadBegin+2, ReadEnd):
    Elements.append(csvData[row][0].replace(' ',''))
    WeightC.append(csvData[row][1].replace(' ',''))
    AtomicC.append(csvData[row][2].replace(' ',''))
del row, ReadBegin, ReadEnd, csvData
# end copying the important data to lists

# convert strings into numbers
AccVol = float(AccVol)
AmpT = float(AmpT)
Lsec = float(Lsec)
for i in range(len(WeightC)):
    WeightC[i] = float(WeightC[i])
    AtomicC[i] = float(AtomicC[i])
del i
# end converting strings into numbers

# calculate uncertainities
WeightU = []
AtomicU = []
for i in range(len(WeightC)):
    if WeightC[i] >= 20:
        WeightU.append(0.02 * WeightC[i])
        AtomicU.append(0.02 * AtomicC[i])
    elif WeightC[i] >= 5:
        WeightU.append(0.04 * WeightC[i])
        AtomicU.append(0.04 * AtomicC[i])
    elif WeightC[i] >= 1:
        WeightU.append(0.2 * WeightC[i])
        AtomicU.append(0.2 * AtomicC[i])
    elif WeightC[i] >= 0.2:
        WeightU.append(WeightC[i])
        AtomicU.append(AtomicC[i])
    else:
        WeightC[i] = 0
        AtomicC[i] = 0
        WeightU.append(WeightC[i])
        AtomicU.append(AtomicC[i])
del i
# end calculating uncertainties

# round, re-normalize, verify 
WeightCTotal = 0
WeightUTotal = 0
AtomicCTotal = 0
AtomicUTotal = 0

for i in range(len(WeightC)):
    WeightC[i] = round(WeightC[i],1)
    WeightU[i] = round(WeightU[i],1)
    AtomicC[i] = round(AtomicC[i],1)
    AtomicU[i] = round(AtomicU[i],1)
    WeightCTotal += WeightC[i]
    WeightUTotal += WeightU[i]
    AtomicCTotal += AtomicC[i]
    AtomicUTotal += AtomicU[i]

WeightCTotal = round(WeightCTotal,1)
WeightUTotal = round(WeightUTotal,1)
AtomicCTotal = round(AtomicCTotal,1)
AtomicUTotal = round(AtomicUTotal,1)

if WeightCTotal != 100.0:
    WeightCTotal -= 100
    WeightC[WeightC.index(max(WeightC))] -= WeightCTotal

if AtomicCTotal != 100.0:
    AtomicCTotal -= 100
    AtomicC[AtomicC.index(max(AtomicC))] -= AtomicCTotal

WeightUMax = max(WeightU)
WeightUTotal -= WeightUMax
if WeightUMax > WeightUTotal:
    WeightU[WeightU.index(WeightUMax)] = WeightUTotal

AtomicUMax = max(AtomicU)
AtomicUTotal -= AtomicUMax
if AtomicUMax > AtomicUTotal:
    AtomicU[AtomicU.index(AtomicUMax)] = AtomicUTotal
    
del i, WeightCTotal, WeightUTotal, WeightUMax
del AtomicCTotal, AtomicUTotal, AtomicUMax
# end rounding, re-normalizing, verifying