# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 04:34:59 2025

@author: LENOVO
"""
from collections import defaultdict
import json
import pandas as pd



df_dirty = pd.read_excel('C:/Users/LENOVO/Desktop/Projects/Bro David/DATA ENTRY-1.xlsx')

df_clean = pd.read_excel('C:/Users/LENOVO/Desktop/Projects/Bro David/Complete data.xlsx')




unique_dept_mappings = defaultdict(set)
for element in zip(df_clean['Department'], df_dirty['Department'][:196]):
    cleaned_key, cleaned_value = element[0].strip().title(), element[1].strip().title()
    unique_dept_mappings[cleaned_key].add(cleaned_value)
    


precious_df_clean = pd.read_csv(r"C:/Users/LENOVO/Desktop/Projects/Precious_excel_file.csv")
precious_df_dirty = pd.read_csv(r"C:/Users/LENOVO/Documents/Precious/DEPARTMENT OF SOCIOLOGY.csv")

precious_df_clean["SD5_Department"] = precious_df_clean["SD5_Department"].str.title().str.strip()
precious_df_dirty["Department "] = precious_df_dirty["Department "].str.title().str.strip()



for element in zip(precious_df_clean['SD5_Department'],precious_df_dirty['Department ']):
    key, value = element[0], element[1]
    unique_dept_mappings[key].add(value)

# Extract from a second dataset
precious_df_clean["SD4_Faculty "] = precious_df_clean["SD4_Faculty "].str.title().str.strip()
precious_df_dirty["Faculty "] = precious_df_dirty["Faculty "].str.title().str.strip()



unique_faculty_mappings = defaultdict(set)
for element in zip(precious_df_clean['SD4_Faculty '],precious_df_dirty['Faculty ']):
    key, value = element[0], element[1]
    unique_faculty_mappings[key].add(value)




#Correcting some duplicate elements
# update method is used because sets are being appended to existing sets

unique_dept_mappings["Archaeology And Anthropology"].update(unique_dept_mappings.pop("Archeology"))
unique_dept_mappings["Communication And Language Arts"].update(unique_dept_mappings.pop("Communication And Language Art"))
unique_dept_mappings["Dentistry"].update(unique_dept_mappings.pop("Dental Surgery"))
unique_dept_mappings["Early Childhood And Educational Foundations"].update(unique_dept_mappings.pop("Early Childhood"))
unique_dept_mappings["Educational Management"].update(unique_dept_mappings.pop("Education Management"))
unique_dept_mappings["Electrical Electronics Engineering"].update(unique_dept_mappings.pop("Electrical And Engineering"))
unique_dept_mappings["English"].update(unique_dept_mappings.pop("English Language"))
unique_dept_mappings["Human Nutrition and Dietetics"] = unique_dept_mappings.pop("Human Nutrition")
unique_dept_mappings["Library, Archival And Informational Sciences"].update(unique_dept_mappings.pop("Laris"))

unique_faculty_mappings["Arts"].update(unique_faculty_mappings.pop("Art"))

# Convert the values of the dictionaries from sets to lists so that they can be json serializable

unique_dept_mappings = {key : list(value) for key, value in unique_dept_mappings.items()}
unique_faculty_mappings = {key : list(value) for key, value in unique_faculty_mappings.items()}

# Save the dictionaries to json
# Saving the files to json
unique_dept_json_str = json.dumps(unique_dept_mappings)
with open("unique_dept_mappings.json", 'w') as dept_file:   
    json.dump(unique_dept_json_str, dept_file)
    
    
unique_faculty_json_str = json.dumps(unique_faculty_mappings)
with open("unique_faculty_mappings.json", 'w') as faculty_file:   
    json.dump(unique_faculty_json_str, faculty_file)


