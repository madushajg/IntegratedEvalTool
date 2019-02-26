

data_testing = open('/media/arshad/Data/FYP/FYP/UserSpecs2PseudoCode/PC_Interface/translations/ipcPythonClean.py')
texts_testing = [line for line in data_testing.readlines() if line.strip()]

print(texts_testing)
