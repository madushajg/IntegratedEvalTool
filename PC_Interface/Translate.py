import sys
import os
import time

f = open('ipc.txt', 'r')
lines = f.readlines()


c = open('sampleRef.pcp', 'r')

statements = c.readlines()

o = open('ipcPythonComplete.txt', 'w+')

for line in lines:
    stmtCount = 0
    for stmt in statements:
        fw = stmt.split(' ', 1)[0]
        #  MULTILINE TRANSLATION
        if fw == '#' or fw == '$':
            stmt = stmt.split(' ', 1)[1]
            compoundStmt = []
            if line == stmt:
                # print(stmt)
                compoundStmt.append(line)
                prevcount = stmtCount - 1
                while True:
                    prevstmt = statements[prevcount]
                    fwpr = prevstmt.split(' ', 1)[0]
                    if fwpr == fw:
                        prevstmt = prevstmt.split(' ', 1)[1]
                        compoundStmt.append(prevstmt)
                        prevcount = prevcount - 1
                    else:
                        break

                compoundStmt.reverse()

                follcount = stmtCount + 1
                while True:
                    follstmt = statements[follcount]
                    fwfl = follstmt.split(' ', 1)[0]
                    if fwfl == fw:
                        follstmt = follstmt.split(' ', 1)[1]
                        compoundStmt.append(follstmt)
                        follcount = follcount + 1
                    else:
                        break

                compoundStmt.reverse()

                while True:
                    o.write(compoundStmt.pop())
                    if len(compoundStmt) == 0:
                        break

                break
        #  SINGLE LINE TRANSLATION
        else:
            if line == stmt:
                # WRITE PSEUDOCODE LINE TO INTERMEDIATE OUTPUT
                o.write(stmt)
                # print(stmt)
                break
        stmtCount = stmtCount + 1


c.close()
o.close()

cr = open('sampleRef.pcr', 'r')

statementsr = cr.readlines()

sr = open('ipcRComplete.txt', 'w+')

for line in lines:
    stmtCount = 0
    for stmt in statementsr:
        fw = stmt.split(' ', 1)[0]
        #  MULTILINE TRANSLATION
        if fw == '#' or fw == '$' or fw == '@':
            stmt = stmt.split(' ', 1)[1]
            compoundStmt = []
            if line == stmt:
                # print(stmt)
                compTok = None
                if fw != '@':
                    compoundStmt.append(line)
                    compTok = fw
                else:
                    compTok = statementsr[stmtCount + 1].split(' ', 1)[0]
                prevcount = stmtCount - 1
                while True:
                    prevstmt = statementsr[prevcount]
                    fwpr = prevstmt.split(' ', 1)[0]
                    if fwpr == compTok:
                        prevstmt = prevstmt.split(' ', 1)[1]
                        compoundStmt.append(prevstmt)
                        prevcount = prevcount - 1
                    else:
                        break

                compoundStmt.reverse()

                follcount = stmtCount + 1
                while True:
                    follstmt = statementsr[follcount]
                    fwfl = follstmt.split(' ', 1)[0]
                    if fwfl == compTok:
                        follstmt = follstmt.split(' ', 1)[1]
                        compoundStmt.append(follstmt)
                        follcount = follcount + 1
                    else:
                        break

                compoundStmt.reverse()

                while True:
                    sr.write(compoundStmt.pop())
                    if len(compoundStmt) == 0:
                        break

                break
        #  SINGLE LINE TRANSLATION
        else:
            if line == stmt:
                # WRITE PSEUDOCODE LINE TO INTERMEDIATE OUTPUT
                sr.write(stmt)
                # print(stmt)
                break
        stmtCount = stmtCount + 1

cr.close()
sr.close()
f.close()

# CALL THE TRANSLATION MODEL.

start = time.time()
if os.path.isfile('ipcPythonComplete.txt'):
    os.system("Travatar/ckylark/src/bin/ckylark --add-root-tag --model Travatar/ckylark/data/wsj " \
              "< ipcPythonComplete.txt > translations/ipcPython.parse.pcp")

    os.system("Travatar/travatar/src/bin/travatar -config_file Travatar/Python/tune/travatar.ini < translations/ipcPython.parse.pcp > translations/ipcPython.translated.out")

if os.path.isfile('ipcRComplete.txt'):
    os.system("Travatar/ckylark/src/bin/ckylark --add-root-tag --model Travatar/ckylark/data/wsj " \
              "< ipcRComplete.txt > translations/ipcR.parse.pcr")

    os.system("Travatar/travatar/src/bin/travatar -config_file Travatar/R/tune/travatar.ini < translations/ipcR.parse.pcr > translations/ipcR.translated.out")

if os.path.isfile("translations/ipcR.translated.out"):
    print('TRANSLATION COMPLETE')
    os.system("python3 translations/CleanTranslation.py translations/ipcPython.translated.out translations/ipcR.translated.out")

end = time.time()
timeElap = end - start
print('finished')
print(timeElap)