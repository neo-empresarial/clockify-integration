import os
import pandas as pd
from datetime import datetime, timedelta
from config import settings
from models import Activity, Client, Member, Project, TimeEntry
#import dateutil.parser as parser
# from __somewherewedunno__ import TimeEntry


def clean_timesheet(df, year):
    '''Clean the timesheet of the year.'''

    header = df.iloc[3]
    header = header[:5].append(header[5:-1].apply(lambda x: x[:5].replace('/','-') + '-' + year))
    df = df[4:]
    df = df.rename(columns = header) 
    df = df.drop(['Curso'], axis=1)
    df = df[df['Integrante'].notnull()]
    df = df[df.columns[:-1]]
    df.update(df.fillna(0))
    return df

def update_TimeEntry(TimeEntry, year, path):
    '''Receive the Time Entry to update with the values of the timesheet in path of the year.'''

    timesheet = pd.read_excel(r'D:\Desktop\UFSC\Monitoramento_de_horas_20191.xlsx')
    timesheet = clean_timesheet(timesheet, '2019')
    timesheet_collumns = list(timesheet.iloc[:, 4:])

    for key, row in timesheet.iterrows():
        member_acronym = row[0]
        project_name = row[1]
        activity_name = row[2]
        client_name = row[3]

        if client_name == 0:
            client_name = "No time" 

        for column in timesheet_collumns:

            if type(row[column]) is str:
                time = float(row[column].replace('ha',''))            
            else:
                time = row[column]

            if activity_name == 0:
                activity_name = ""

            if time > 0:
                time_hours = (time * 50) // 60
                time_minutes = (time * 50) % 60
                start = datetime.strptime(column, "%d-%m-%Y")-timedelta(days = 1)
                end = start+timedelta(hours=time_hours, minutes=time_minutes)

                TimeEntry = TimeEntry.append({'member_acronym': member_acronym, 'project_name': project_name,
                                'activity_name': activity_name, 'client_name': client_name,
                                'start': start, 'end': end}, ignore_index=True)
    
    return TimeEntry

def get_member_id(acronym):
    try:
        member_id = Member.where("acronym", acronym).first().id

    except:
        email = acronym.swapcase() + "@certi.org.br"
        Member.update_or_create({"acronym": acronym},
                                {"clockify_id": acronym,
                                "email": email})
        member_id = Member.where("acronym", acronym).first().id

    return member_id

def get_project_id(name):
    try:
        project_id = Project.where("name", name).first().id

    except:
        Project.update_or_create({"clockify_id": ""}, {"name": name})
        project_id = Project.where("name", name).first().id

    return project_id

def get_activity_id(name):
    try:
        activity_id = Activity.where("name", name).first().id

    except:
        Activity.update_or_create({"name": name})
        activity_id = Activity.where("name", name).first().id

    return activity_id

def get_client_id(name):
    try:
        client_id = Client.where("name", name).first().id

    except:
        Client.update_or_create({"clockify_id": ""}, {"name": name})
        client_id = Client.where("name", name).first().id

    return client_id

def update_TimeEntry_ids(TimeEntry, member_ids, project_ids, activity_ids, client_ids):

    for key, row in TimeEntry.iterrows():
        new_row = []
        for member_acronym, member_id  in member_ids.items():
            if member_acronym == row[0]:
                TimeEntry.iloc[key, 1] = member_id
                break

        for project_name, project_id  in project_ids.items():
            if project_name == row[2]:
                TimeEntry.iloc[key, 3] = project_id
                break
        
        for activity_name, activity_id  in activity_ids.items():
            if activity_name == row[4]:
                TimeEntry.iloc[key, 5] = activity_id
                break
        
        for client_name, client_id  in client_ids.items():
            if client_name == row[6]:
                TimeEntry.iloc[key, 7] = client_id
                break
        
    return TimeEntry

def import_timesheets():
    header_TimeEntry = {'member_acronym': '', 'member_id': '', 'project_name': '',
                     'project_id': '', 'activity_name': '','activity_id': '',
                     'client_name': '', 'client_id': '', 'start': '', 'end': ''}

    TimeEntry = pd.DataFrame(columns=header_TimeEntry)
    TimeEntry = update_TimeEntry(TimeEntry, '2019', 'path')
    
    member_ids = {}
    members_acronym = TimeEntry.member_acronym.unique()
    for acronym in members_acronym:
        member_ids[acronym] = get_member_id(acronym)

    project_ids = {}
    project_names = TimeEntry.project_name.unique()
    for name in project_names:
        project_ids[name] = get_project_id(name)
    
    activity_ids = {}
    activity_names = TimeEntry.activity_name.unique()
    for name in activity_names:
        activity_ids[name] = get_activity_id(name)
    
    client_ids = {}
    client_names = TimeEntry.client_name.unique()
    for name in client_names:
        client_ids[name] = get_client_id(name)
    
    TimeEntry = update_TimeEntry_ids(TimeEntry, member_ids, project_ids,
                                    activity_ids, client_ids)
    
    TimeEntry.to_csv(r'D:\Desktop\TimeEntry.csv')
if __name__ == '__main__':
    import_timesheets()