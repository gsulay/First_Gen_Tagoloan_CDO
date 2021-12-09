import numpy as np
import pandas as pd
import re

def timestamp_conv(timestamp):
    timestamp=timestamp.split()
    date=timestamp[0]
    time=timestamp[1]
    hms=time.split(':')
    if len(timestamp)==3:
        morn_aft=timestamp[2]
        if int(hms[0])==12 and morn_aft=='AM':
            hour=0
        elif int(hms[0])==12 and morn_aft=='PM':
            hour=12
        elif morn_aft=='PM':
            hour=int(hms[0])+12
        elif morn_aft=='AM':
            hour=int(hms[0])

    if len(timestamp)==2:
        hour=int(hms[0])
    #reorganized timestamp to y/m/d
    date_split=date.split('/')
    month=date_split[0]
    day=date_split[1]
    year=date_split[2]
    reorganized_date=f"{int(year)}/{int(month)}/{int(day)}"
    new_timestamp=f"{reorganized_date} {int(hour)}:00:00"
    return new_timestamp

def duplicates_df(df):
    try:
        new_df = pd.concat([g for _, g in df.groupby("Timestamp") if len(g) > 1])
        return new_df
    except:
        new_df = df.iloc[0:0]
        return new_df
    
def hours_only(df):
    timestamp_arr=df['Timestamp']
    hour_lst=[]
    for i in timestamp_arr:
        time=i.split()[1]
        hour=time.split(':')[0]
        hour_lst.append(hour)
    df['Hour']=hour_lst
    return df

def check_integrity(df):
    return df[df.isnull().any(axis=1)]

def clean_water_level(corrected_df, diff_limit = 0.5):
    water_level = corrected_df['Corrected_Water_Level']
    #diff limit determines whether the difference is erroneous if difference is more than diff limit then data is erroneous
    is_erroneous=[0]
    count = 1
    
    for i in water_level[1:]:
        val = i-water_level[count - 1]
        val = abs(val)
        if val >= diff_limit:
            is_erroneous.append(1)
        else:
            is_erroneous.append(0)
        count += 1
    corrected_df['err_check']=is_erroneous
    corrected_df['Corrected_Water_Level'] =corrected_df['Corrected_Water_Level'].loc[corrected_df['err_check']==1]
    edited_water_level=corrected_df.loc[:, 'Corrected_Water_Level']
    final_water_level=edited_water_level.astype('float64').interpolate()
    corrected_df=corrected_df.drop(columns=['Corrected_Water_Level','err_check'])
    corrected_df['Corrected_Water_Level']=final_water_level
    print(final_water_level)
    return corrected_df