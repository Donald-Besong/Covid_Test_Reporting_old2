import iterdata
import main_argparser
import argparse
from datetime import datetime, date
from itertools import tee
import pandas as pd
import copy
import numpy as np
pd.options.mode.chained_assignment = None
import math

#*****************begin reading arguments
data_source = main_argparser.data_source
name = main_argparser.name
strip_id = main_argparser.strip_id
value = main_argparser.value
which_test = main_argparser.which_test  
#*****************end reading arguments

x = iterdata.IterData(data_source)
x.iterRead()
dataSet1 = x._dataSet1
dataSet2 = x._dataSet2
dataSet3 = x._dataSet3

message = "hello there"
dataSet1Rows = dataSet1.rows
dataSet2Rows = dataSet2.rows
dataSet3Rows = dataSet3.rows
	
def get_length(x):
	i = 0
	row_data = next(x, None)
	while row_data:
		row = [cell.value for cell in row_data]
		if not row[0] and row[0] != 0:
			return(i)
		row_data = next(x, None)
		i += 1
	return(i)

dataSet1Rows_glob, dataSet1Rows_d = tee(dataSet1Rows)
d1 = get_length(dataSet1Rows_d)
		
dataSet2Rows_glob, dataSet2Rows_d = tee(dataSet2Rows)
d2 = get_length(dataSet2Rows_d)	

dataSet3Rows_glob, dataSet3Rows_d = tee(dataSet3Rows)
d3 = get_length(dataSet3Rows_d)

def createList(data, n):
	row_data = next(data, None)[0].value
	data_list = []
	for i in range(1, n):
		row_data = next(data, None)[0].value
		data_list.append(row_data)
	return data_list

Set1 = createList(dataSet1Rows_glob, d1)
Set2 = createList(dataSet2Rows_glob, d2)
Set3 = createList(dataSet3Rows_glob, d3)
			
def covidResult(strip_id, v):
    result = ""
    success = 0
    if strip_id in Set1:
        print(f'Hello {name}. Your strip id was {strip_id}, and your value is {v} in S1.')
        if v == '100':
            success = success + 1
            result = "Your result is negative."
        elif v == '110':
            result = "Your result is positive."
        else:
            result = "undefined - please repeat test."
    elif strip_id in Set2:
        print(f'Hello {name}. Your strip id was {strip_id}, and your value is {v} in S2.')
        if v == '010':
            success = success + 1
            result = "Your result negative."
        elif v == '011':
            result = "Your result positive."
        else:
            result = "undefined - please repeat test"
    elif strip_id in Set3:
        print(f'Hello {name}. Your strip id was {strip_id}, and your value is {v} in S3.')
        if v == '001':
            success = success + 1
            result = "Your result negative."
        elif v == '101':
            result = "Your result positive."
        else:
            result = "undefined - please repeat test"
    else:
        result = "The strip id is invalid"
    return result
    
			
def testCheater(strip_id, v):
    success = 0
    total = 1
    if strip_id in Set1:
        if v == '100':
            success = 1
    elif strip_id in Set2:
        if v == '010':
            success = 1
    elif strip_id in Set3:
        if v == '001':
            success = 1
    return success, total
    	    
if __name__ == '__main__':
    success = 0
    total = 0
    if which_test == "test1":
        test = covidResult(strip_id, value)
        print(test)
    elif which_test == "test2":
        while total < 5:
            strip_id = input("Enter strip id:")
            value = input("Enter value:")
            output = testCheater(strip_id, value)
            success = success + output[0]
            total = total + output[1]
        print('\n ****************************')
        print(f'total={total} and success={success}')
        print('****************************')
    else:
        print("Sorry, we do not offer the requested test.")
        
    

    
		
		

    




