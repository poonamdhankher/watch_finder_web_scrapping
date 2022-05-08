import pandas as pd
import glob
import os
import csv


fout=open("/Users/poonamdhankher/Downloads/test/8orn Task/watch_output.csv","a") 
for num in range(1,85):
    f = open("/Users/poonamdhankher/Downloads/test/8orn Task/watches_data"+str(num)+".csv")
    next(f)
    for line in f:
         fout.write(line)
    f.close() # not really needed
fout.close()