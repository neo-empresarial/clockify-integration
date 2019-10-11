import os
import pandas as pd
from datetime import datetime, timedelta
#import dateutil.parser as parser
# from __somewherewedunno__ import TimeEntry


def clean_timesheet(df, year):

    header = df.iloc[3]
    header = header[:5].append(header[5:-1].apply(lambda x: x[:5].replace('/','-') + '-' + year))
    df = df[4:]
    df = df.rename(columns = header) 
    df = df.drop(['Curso'], axis=1)
    df = df[df['Integrante'].notnull()]
    df = df[df.columns[:-1]]
    df.update(df.fillna(0))
    return df

header_TimeEntry = {'member_acronym': '', 'member_id': '', 'project_name': '',
                     'project_id': '', 'activity_name': '','activity_id': '',
                     'client_name': '', 'client_id': '', 'start': '', 'end': ''}

TimeEntry = pd.DataFrame(columns=header_TimeEntry)

timesheet = pd.read_excel(r'D:\Desktop\UFSC\Monitoramento_de_horas_20191.xlsx')
timesheet = clean_timesheet(timesheet, '2019')
timesheet_collumns = list(timesheet.iloc[:, 4:6])

for key, row in timesheet.iterrows():
    member_acrony = row[0]
    project_name = row[1]
    activity_name = row[2]
    client_name = row[3]

    for column in timesheet_collumns:
        if row[column] > 0:
            print('here')
            time_hours = (row[column] * 50) // 60
            time_minutes = (row[column] * 50) % 60
            start = datetime.strptime(column, "%d-%m-%Y")-timedelta(days = 1)
            end = start+timedelta(hours=time_hours, minutes=time_minutes)

            TimeEntry = TimeEntry.append({'member_acrony': member_acrony, 'project_name': project_name,
                            'activity_name': activity_name, 'client_name': client_name,
                            'start': start, 'end': end}, ignore_index=True)
print(TimeEntry)