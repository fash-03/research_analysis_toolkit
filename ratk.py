# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 02:43:30 2025

@author: LENOVO
"""

''' This module is a set of helper functions for analysing undergraduate research and survey data'''


import pandas as pd
from rapidfuzz.process import extractOne
import json


def read_csv(filepath, *kwargs):
    ''' Wrapper function for pd.read_csv and returns a Dataset class object '''
    
    data = pd.read_csv(filepath, *kwargs)
    return Dataset(data)

with open("unique_faculty_mappings.json", 'r') as faculty_file:   
    unique_faculty_mappings_dict = json.loads(json.load(faculty_file))

with open("unique_dept_mappings.json", 'r') as dept_file:   
    unique_dept_mappings_dict = json.loads(json.load(dept_file))
    
class Dataset(pd.DataFrame):
    DEPT_MAP = unique_dept_mappings_dict
    FACULTY_MAP = unique_faculty_mappings_dict


    def __init__(self, df):
        
        super().__init__(df)
        
        
        
    def clean_google_sheets(self):
        return self.drop(["Timestamp", "Email Address"], axis=1, inplace=True)
    
    def clen_column_names(self):
        self.columns = [column.strip() for column in self.columns]
        return self
    
    def clean_dept_column(self, dept_column=None):
        if dept_column is None:
            dept_column = "Department"
        self[dept_column] = self[dept_column].str.strip().str.title()
        
        dept_names = self[dept_column]
        for dept_name in dept_names:
            if dept_name in unique_dept_mappings_dict.keys():
                continue
            else:
                closest_match = extractOne(dept_name, unique_dept_mappings_dict) 
                # use score_cutoff method of extractOne if results are not reasonable
                response = input(f"Is {closest_match[0]} the correct department name for {dept_name}? y/n")
                if response.strip().lower() == "y":
                    # Add the incorrect value to the mapping and then update the dept_name to the correct value
                    correct_match = closest_match[0]
                    unique_dept_mappings_dict[correct_match].append(dept_name)
                    
                    # Update its value in the list
                    index = dept_names.index(dept_name)
                    dept_names[index] = correct_match
                elif response.strip().lower() == "n":
                    res = input("What is the correct department name for {dept_name} then? [Input 's' or 'skip' to skip this instance")
                    if res.strip().lower() in ["s", "skip"]:
                        continue
                    else:
                        # Update with the value that is provided
                        index = dept_names.index(dept_name)
                        dept_names[index] = res
                    
                    
        self[dept_column] = dept_names
        return self
            
    def clean_faculty_column(self, faculty_column=None):
        if faculty_column is None:
            faculty_column = "Faculty"
        
        self[faculty_column] = self[faculty_column].str.strip().str.title()
           
    def sectionize(self, demographics_section=0):
        pass
    
    def code_values(self, order=None):
        pass
    
    def set_value_labels(self):
        pass
    
    def output_spss_file(self, filepath):
        pass
    
    def run_demographics_summary(self):
        pass
    
    def output_to_excel(self):
        pass
        
        
        
df = Dataset(pd.read_csv(r'C:\Users\LENOVO\Downloads\Chrome Downloads\Japheth_friend_data.csv'))



df.head()
df.clean_google_sheets()
