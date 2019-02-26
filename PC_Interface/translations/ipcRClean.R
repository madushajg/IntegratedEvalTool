library ( tidyverse )
df <- TRUE 'videogamesales.csv' = read_csv file )
fileConn <- file("RResults.txt")
array <- vector()
start <- Sys.time()
clf <- train ( df_test ~ . , Genre , set test , df_train )
end <- Sys.time()
timeElap <- end - start
timeElap <- as.character(timeElap)
time <- paste('time', timeElap, sep=" ")
array <- c(array, timeElap)
predictions <- predict ( clf )
y_test <- unlist ( y_test )
predictions <- unlist ( predictions )
cm <- table ( y_test , predictions )
accuracy <- cm ) diag ) sum / length ( y_test ) get )
accuracy <- as.character(accuracy)
acc <- paste('accuracy', accuracy, sep=" ")
array <- c(array, accuracy)
target_class <- 'Genre'
split <- 0.75
features <- c ( 'Rank', 'Name', 'Platform', 'Year', 'Publisher', 'NA_Sales' )
ratio <- sample df ) n = nrow ( df , sample 0.75 = ) n = nrow ( assign )
X <- df [ features ]
y <- df [ target_class ]
df_train <- df [ ratio , ]
df_test <- df [ - ratio , ]
X_train <- X [ ratio , ]
X_test <- X [ - ratio , ]
y_train <- y [ ratio , ]
y_test <- y [ - ratio , ]
writeLines(array, fileConn)
close(fileConn)