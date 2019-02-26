import sys
import json

arg = sys.argv

pythonFile = open(arg[1], 'r')
RFile = open(arg[2], 'r')

lines = pythonFile.readlines()
linesr = RFile.readlines()

outputPyFName = arg[1].split('.')
outputRFName = arg[2].split('.')

op = open(outputPyFName[0]+'Clean.py', 'w+')
sr = open(outputRFName[0]+'Clean.R', 'w+')

wildcards = open('/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/wildcard.json').read()

data = json.loads(wildcards)

op.write('import time\n')
pythonClassifier = False
for line in lines:
    for object in data:
        if object in line:
            if type(data[object]) is not str:
                if type(data[object]) is list:
                    listString = ''
                    first = True
                    for item in data[object]:
                        if first:
                            first = False
                        else:
                            listString += ', '
                        if type(item) is str:
                            listString += '\''+item+'\''
                        else:
                            listString += str(item)
                    line = line.replace(object, listString)
                else:
                    line = line.replace(object, str(data[object]))
            else:
                line = line.replace(object, data[object])
    if 'fit' in line:
        if not pythonClassifier:
            op.write('out = open(\'pythonResults.txt\', \'w+\')\n')
        op.write('start = time.time()\n')
        op.write(line)
        op.write('end = time.time()\n')
        op.write('timeElap = end - start\n')
        op.write('out.write(\'time \'+str(timeElap))\n')
        pythonClassifier = True
    elif 'accuracy' in line:
        op.write(line)
        op.write('out.write(\'accuracy \'+str(accuracy))\n')
    else:
        op.write(line)

if pythonClassifier:
    op.write('out.close()\n')
pythonFile.close()
op.close()

RClassifier = False
for liner in linesr:
    for object in data:
        if object in liner:
            if type(data[object]) is not str:
                if type(data[object]) is list:
                    listString = ''
                    first = True
                    for item in data[object]:
                        if first:
                            first = False
                        else:
                            listString += ', '
                        if type(item) is str:
                            listString += '\''+item+'\''
                        else:
                            listString += str(item)
                    liner = liner.replace(object, listString)
                else:
                    liner = liner.replace(object, str(data[object]))
            else:
                liner = liner.replace(object, data[object])
    if '~' in liner:
        if not RClassifier:
            sr.write('fileConn <- file("RResults.txt")\n')
        sr.write('array <- vector()\n')
        sr.write('start <- Sys.time()\n')
        sr.write(liner)
        sr.write('end <- Sys.time()\n')
        sr.write('timeElap <- end - start\n')
        sr.write('timeElap <- as.character(timeElap)\n')
        sr.write('time <- paste(\'time\', timeElap, sep=" ")\n')
        sr.write('array <- c(array, timeElap)\n')
        RClassifier = True
    elif 'accuracy' in liner:
        sr.write(liner)
        sr.write('accuracy <- as.character(accuracy)\n')
        sr.write('acc <- paste(\'accuracy\', accuracy, sep=" ")\n')
        sr.write('array <- c(array, accuracy)\n')
    else:
        sr.write(liner)

if RClassifier:
    sr.write('writeLines(array, fileConn)\n')
    sr.write('close(fileConn)')

RFile.close()
sr.close()
print('finished')