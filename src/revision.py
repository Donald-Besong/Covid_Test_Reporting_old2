import iterdata
import dataanalysis
import main_argparser
from datetime import datetime, date
from itertools import tee
import pandas as pd
import copy
import numpy as np
pd.options.mode.chained_assignment = None
import math

#*****************begin reading arguments
data_source = main_argparser.data_source
print(data_source)
risk_rating = main_argparser.risk_rating
cutoff_date_glob = main_argparser.cutoff_date
dob_filter_glob = main_argparser.dob_filter
fee_str = main_argparser.fee_str
test_number = main_argparser.testNumber   
#*****************end reading arguments

x = iterdata.IterData(data_source)
x.iterRead()

dataSet1 = x._dataSet1 #openpyexel object
dataSet2 = x._dataSet2
trnsData = x._trnsData
feeTypeMapping = x._feeTypeMapping

message = "hello there"
dataSet1Rows = dataSet1.rows #iterator
dataSet2Rows = dataSet2.rows
trnsDataRows = trnsData.rows
feeTypeMappingRows = feeTypeMapping.rows

def get_length(x):
	i = 0
	row_data = next(x, None)
	while row_data:
		row = [cell.value for cell in row_data]
		if not row[0] and row[0] != 0: #this is because None false, and 0 is also false
            #i had earlier explored the data and seen that the last rows are emty
            #thid check ensures that I do not count the last emty row.
			return(i)
		row_data = next(x, None)
		i += 1
	return(i)

def analyse(x): #this is no longer neede as it was just an
    #ad-hoc tool for cleansing and exploration, to see what is in the nulls
	i = 0
	row_data = next(x, None)
	while row_data:
		row = [cell.value for cell in row_data]
		if not row[0]:
			return 
		print(i)
		print(row)
		row_data = next(x, None)
		i += 1
        
dataSet2Rows_glob, dataSet2Rows_d = tee(dataSet2Rows) #this creates two copies of 
            #the iterator
            #and this is needed because get_length advances the first and would 
            #not be re-usable. The second copy was used for exploration
d = get_length(dataSet2Rows_d)

dataSet1Rows_glob, dataSet1Rows_d = tee(dataSet1Rows)
d1 = get_length(dataSet1Rows_d)	

dataTurns_glob, dataTurns_d = tee(trnsDataRows)
d_turns = get_length(dataTurns_d)

feeType_glob, feeType_d = tee(feeTypeMappingRows)
d_feeType = get_length(feeType_d)

def dataPreDataSet2(): #this is no longer neede as it was just an
    #ad-hoc tool for cleansing and exploration
	i = 0
	x2 = iterdata.IterData(data_source) #read afresh. after-all it is efficient
	x2.iterRead()
	dataSet2_firstCopy = x2._dataSet2
	dataSet2Rows_firstCopy = dataSet2_firstCopy.rows
	row_data = next(dataSet2Rows_firstCopy, None)
	missing = []
	non_date = []
	
	missing_txt = open("missing.txt", "w")
	non_date_txt = open("non_date.txt", "w")
	while i < d:
		row = [cell.value for cell in row_data]
		row_str = [str(cell.value) for cell in row_data]
		if not row[0] or not row[1] or not row[2]:
			missing.append((i,row))
			txt = ",".join((",".join(row_str), str(i)))
			if i > 0: #dont read the header
				missing_txt.write(txt + "\n")
		if not isinstance(row[2], date):
			non_date.append((i,row))
			txt = ",".join((",".join(row_str), str(i)))
			if i > 0:
				non_date_txt.write(txt + "\n")
		row_data = next(dataSet2Rows_firstCopy, None) 
		i += 1
	missing_txt.close()
	non_date_txt.close()
	return missing
    
def createDF(data, n):
	row_data = next(data, None)
	row = [cell.value for cell in row_data]
	headers = row
	data_list = []
	for i in range(1, n):
		row_data = next(data, None)
		row = [cell.value for cell in row_data]
		data_list.append(row)
	df = pd.DataFrame(data_list, columns=headers)
	return df

#1. Find the cst_numbers of people of high risk_rating (or the rating we desire),
#   who were assessed earlier than cutoff_date_glob
def riskReviewDate(): 
	x2 = iterdata.IterData(data_source) 
	x2.iterRead()
	dataSet2_thirdCopy = x2._dataSet2
	dataSet2Rows_thirdCopy = dataSet2_thirdCopy.rows
	dataSet2_df = createDF(dataSet2Rows_thirdCopy, d)
	
	cutoff_date = datetime.strptime(cutoff_date_glob, "%d/%m/%Y")
	#print(dataSet2_df)
	#print(dataSet2_df.shape)
	print("cutoff_date = %s" % cutoff_date)
	
	print("***************begin cleansing")
	#dataSet2_df***
	#print(dataSet2_df.head())
	#print(dataSet2_df.describe())
	#print(dataSet2_df.DATE_LAST_ASSESSED.describe())
	#print(dataSet2_df.dtypes)
	d_shape = dataSet2_df.shape
	#print(d_shape)
	for i in range(d_shape[0]):
		if not isinstance(dataSet2_df.DATE_LAST_ASSESSED.iloc[i], date):
			#dataSet1_df.DOB.iloc[i] = datetime.strptime(dataSet1_df.DOB.iloc[i], "%d/%m/%Y")
			print(dataSet2_df.DATE_LAST_ASSESSED.iloc[i]) #exploration only
			
	for i in range(d_shape[0]):
		if not isinstance(dataSet2_df.RISK_RATING.iloc[i], str):
			#dataSet1_df.DOB.iloc[i] = datetime.strptime(dataSet1_df.DOB.iloc[i], "%d/%m/%Y")
			print(dataSet2_df.RISK_RATING.iloc[i]) #exploration only
			
			
	for i in range(d_shape[0]):
		if not isinstance(dataSet2_df.CST_NUMBER.iloc[i], np.int64):
			#dataSet1_df.DOB.iloc[i] = datetime.strptime(dataSet1_df.DOB.iloc[i], "%d/%m/%Y")
			print(dataSet2_df.CST_NUMBER.iloc[i])
	print("***************end cleansing")
			
	dataSet2_df_final = dataSet2_df.loc[dataSet2_df.DATE_LAST_ASSESSED <  cutoff_date]
	dataSet2_df_final.RISK_RATING = dataSet2_df_final.RISK_RATING.str.lower()
	dataSet2_df_final2 = dataSet2_df_final.loc[dataSet2_df_final.RISK_RATING == risk_rating.lower()]		
	#print(dataSet2_df)
	#print(dataSet2_df_final2)
	cst_List = dataSet2_df_final2.CST_NUMBER.tolist()
	print("\n \n The answer to question 1 is:")
	print(cst_List)
    
#2. Find the cst_numbers of people born after 01/09/2003 who took an overdraft
def overDraft(): 		
	dob_filter = datetime.strptime(dob_filter_glob, "%d/%m/%Y")
	today = datetime.strptime('05/12/2021', "%d/%m/%Y")
	print(dob_filter)
	print("fee descr string = %s, dob = %s" % (fee_str, dob_filter))
	id_list = []
	x1 = iterdata.IterData(data_source)
	x1.iterRead()
	
	dataSet1_thirdCopy = x1._dataSet1
	dataSet1Rows_thirdCopy = dataSet1_thirdCopy.rows
	dataSet1_df = createDF(dataSet1Rows_thirdCopy, d1)

	trnsData_thirdCopy = x1._trnsData
	trnsDataRows_thirdCopy = trnsData_thirdCopy.rows
	trnsData_df = createDF(trnsDataRows_thirdCopy, d_turns)	
	
	feeTypeMapping_thirdCopy = x1._feeTypeMapping
	feeTypeMappingRows_thirdCopy = feeTypeMapping_thirdCopy.rows
	feeType_df = createDF(feeTypeMappingRows_thirdCopy, d_feeType)
	
	#***********begin cleansing*************
	#dataSet1_df***
	#print(dataSet1_df.head())
	#print(dataSet1_df.describe())
	#print(dataSet1_df.DOB.describe())
	#print(dataSet1_df.dtypes)
	d_shape = dataSet1_df.shape
	#print(d_shape)
	for i in range(d_shape[0]):
		if not isinstance(dataSet1_df.DOB.iloc[i], date) and dataSet1_df.DOB.iloc[i] != '=#VALUE!':
			dataSet1_df.DOB.iloc[i] = datetime.strptime(dataSet1_df.DOB.iloc[i], "%d/%m/%Y")
			
	#print(dataSet1_df.describe())
	#print(dataSet1_df.DOB.describe())
	dataSet1_df = dataSet1_df[dataSet1_df.DOB != '=#VALUE!']
	dataSet1_df = dataSet1_df[dataSet1_df.DOB > dob_filter]
	dataSet1_df = dataSet1_df[dataSet1_df.DOB < today]
	#print(dataSet1_df.shape)
	#print(dataSet1_df.DOB.describe())
	#print(min(dataSet1_df.DOB))
	
	#trnsData_df*****
	trnsData_df = trnsData_df[['CST_NUMBER','FEE_TYPE']]
	dtrns_shape = trnsData_df.shape
	#print(dtrns_shape)
	#print(trnsData_df.head())
	#print(trnsData_df.describe())
	#print(trnsData_df.CST_NUMBER.describe())
	#print(trnsData_df.FEE_TYPE.describe())

	#for i in range(dtrns_shape[0]):
		#if not isinstance(trnsData_df.FEE_TYPE.iloc[i], np.float64) or math.isnan(trnsData_df.FEE_TYPE.iloc[i]):
			#print(i)
			#print(type(trnsData_df.FEE_TYPE.iloc[i]))
			#print(trnsData_df.FEE_TYPE.iloc[i])
	trnsData_df = trnsData_df.dropna()
	#print(trnsData_df.shape)
	
	#feeType_df*****
	fee_numbers = []
	feeType_df = feeType_df[['Fee Code', 'Fee Description']]
	for i in range(feeType_df.shape[0]):
		if fee_str.lower() in (feeType_df.loc[i]['Fee Description']).lower():
			fee_numbers.append(feeType_df.loc[i]['Fee Code'])
		
	#print(fee_numbers)
	
	trnsData_df = trnsData_df.loc[trnsData_df.FEE_TYPE.isin (fee_numbers)]
	#print(trnsData_df)
	#print(dataSet1_df)
	#final_merge = pd.merge(trnsData_df, dataSet1_df, how="inner", on=[trnsData_df.CST_NUMBER, dataSet1_df.CS_NUMBER])
	#print(final_merge)
	trns_CST_NUMBER = trnsData_df['CST_NUMBER'].tolist()
	Set1_CS_NUMBER = dataSet1_df['CS_NUMBER'].tolist()
	#print(len(trns_CST_NUMBER))
	#print(len(Set1_CS_NUMBER))
	final_list = set(trns_CST_NUMBER).intersection(set(Set1_CS_NUMBER))
	#print(len(final_list))
	print("\n \n The answer to question 2 is:")
	print(final_list) #this is the anwer needed
	#***********end cleansing*************			
	    
if __name__ == '__main__':
	if test_number == 1:
		riskReviewDate()
	elif test_number == 2:
		overDraft()
	else:
		print("Test number does not exist")
