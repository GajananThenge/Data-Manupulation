# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 11:07:15 2019

@author: gthenge
"""

import pandas as pd
import numpy as np
import os


src_dir = r"C:\Users\gthenge\Desktop\Krishna\Input"
dst_file = r"C:\Users\gthenge\Desktop\Krishna\Output\Output.csv"
out_filename=r"C:\Users\gthenge\Desktop\Krishna\Program_output.csv"

def get_file_names(dirName):
    import os
    all_files=[]
    file_paths=os.listdir(dirName)
    for p in file_paths:
        full_path=os.path.join(dirName,p)
        if os.path.isdir(full_path):
            all_files=all_files+get_file_names(full_path)
        else:
            all_files.append(full_path)
    return all_files

def combined_data(dirName,out_file_name=None):
    result_df =pd.DataFrame()
    #allfiles=get_file_names(dirName)
    print("="*60)
    print("Combining files :")
    csv_files  = [ f for f in get_file_names(dirName) if f.endswith('.csv')]
    for f in csv_files:
        print(f)
        df = pd.read_csv(f,delimiter=',',low_memory=False)
        result_df=result_df.append(df)
    if out_file_name:
        result_df.to_csv(out_file_name,index=False)
    return result_df


# =============================================================================
# Return Combined File if file name not mentioned it wont save combine data file
# =============================================================================
com_df = combined_data(src_dir,out_file_name=r"C:\Users\gthenge\Desktop\Krishna_combined.csv")

out_df = pd.read_csv(dst_file,header=0)

com_df.columns
# =============================================================================
# ['Alarm Tag', 'Alarm Description', 'Alarm State', 'Pr', 'Group', 'Cause',
#       'Effect', 'Required Response', 'Control System Response', 'Masking',
#       'Vector To', 'Units', 'Min', 'Max', 'Set point', 'Dead band',
#       'Filter Time', 'Unnamed: 17']
# =============================================================================


out_df.columns
# =============================================================================
# ['Device', 'Alarm Tag', 'Alarm Description', 'Alarm State', 'Pr',
#       'Group', 'Rationale', 'Cause', 'Unnamed: 8', 'Unnamed: 9',
#       'Unnamed: 10', 'Unnamed: 11', 'Effect', 'Required Response',
#       'Control System Response', 'Masking', 'Unnamed: 16', 'Unnamed: 17',
#       'Unnamed: 18', 'Unnamed: 19', 'Units', 'Min', 'Max', 'Set point',
#       'Dead band', 'Filter Time']
# =============================================================================


selected_features =[ 'Alarm Description', 'Alarm State', 'Pr',
       'Group', 'Cause']


duplicate_records = com_df[com_df.duplicated(subset=['Alarm Tag'])]
##drop Duplicate Alarm Tag if any from Combine data
com_df.drop_duplicates(subset ="Alarm Tag", 
                      inplace = True) 


out_df.loc[out_df["Alarm Tag"].isin(com_df["Alarm Tag"]), selected_features] = com_df[selected_features]

out_df.to_csv(out_filename,index=False)
