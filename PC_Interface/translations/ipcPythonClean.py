import time
import pandas as pd
cm = confusion_matrix ( y_test , predictions )
df = pd . read_csv ( 'videogamesales.csv' )
out = open('pythonResults.txt', 'w+')
start = time.time()
clf = ( X_train , y_train neighbors ( ) . fit )
end = time.time()
timeElap = end - start
out.write('time '+str(timeElap))
target_class = 'Genre'
split = 0.75
features = [ 'Rank', 'Name', 'Platform', 'Year', 'Publisher', 'NA_Sales' ]
df [ 0.75 train_test_split , df . set = target ( = X_train , X_test , y_train , y_test )
cm = confusion_matrix ( y_test , predictions )
out.close()
