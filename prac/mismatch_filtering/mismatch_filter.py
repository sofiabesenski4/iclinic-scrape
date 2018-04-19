#mismatch_filter.py
import re
import os
from pg import DB
import datetime
from insert_screens_into_db import insert_patient_set_into_db
"""
function API:           insert_patient_set_into_db(db_ptr, dup_ptr, patient_set):
					returns none
#tuples are of the form: (new_patient_phn,new_patient_first_name,new_patient_last_name,new_patient_dob_datetime_obj)

"""

def filter_and_insert():
	#mismatches.txt is the remaining patients which were not captured by the regular expression, but could still represent valid patients
	fp = open("mismatches.txt", "r")
	#mismatches2.txt contains the patients who did have a 10 digit phn, but were not recognized by the filter 2 or 3
	fp_2 = open("mismatches2.txt", 'w')
	#duplicate_filtered_entries.txt contains the entries which were successfully recognized by filters 2 or 3, but had an already existing phn in the database
	dup_fp = open("duplicate_filtered_entries.txt", "w")
	filtered_patients = set()
	nonmatches = []
	filter1 = re.compile(r'\d{10}')
	filter2 = re.compile(r'([\S]*)[,.]([\S]*) (\d{10}) (\d{2}/\d{2}/\d{4})')
	filter3 = re.compile(r'([\S]*) (\d{10}) (\d{2}/\d{2}/\d{4})')
	#firstly filter out the entries which do not contain any 10 digit phn therefore they are irrelevant to our procedure
	
	patient_set = set()
	for line in fp:
		if re.search(filter1,line):
			filtered_patients.add(line)

#	print(len(list(filtered_patients)))		

	#now filtered_patients has only entries with a 10 digit PHN
	for patient_line in filtered_patients:
		if re.search(filter2,patient_line):
			print (str(re.search(filter2,patient_line)))
			temp_date = str(re.search(filter2,patient_line).group(4)).split("/")
			temp_date = temp_date[2]+"-"+temp_date[0]+"-"+temp_date[1]
			patient_set.add((re.search(filter2,patient_line).group(3),re.search(filter2,patient_line).group(1),re.search(filter2,patient_line).group(2),temp_date))
		else:
			if re.search(filter3,patient_line):
				
				temp_date = str(re.search(filter3,patient_line).group(3)).split("/")
				temp_date = temp_date[2]+"-"+temp_date[0]+"-"+temp_date[1]
				patient_set.add((re.search(filter3,patient_line).group(2),None,re.search(filter3,patient_line).group(1),temp_date))
		
			#insert into db using (phn, null,last_name, DOB) format where last_name is the concatenated firstname and lastname found by the OCR
			else:
				#still entries which were not captured by one of filter2 or filter3
				nonmatches.append(patient_line)
	print("the number of recognized mismatches to be added is " + str(len(list(filtered_patients))))
	#insert_patient_set_into_db(DB("test_patients"),dup_fp,patient_set)
if __name__ == "__main__":
	filter_and_insert()
		
