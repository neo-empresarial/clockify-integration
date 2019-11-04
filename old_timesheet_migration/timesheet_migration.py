import os
import glob
import pandas as pd
import sys
from datetime import datetime, timedelta
from os.path import dirname, join, exists, abspath

sys.path.append('../')
from config import settings
from models import Activity, Client, Member, Project, TimeEntry

def clean_timesheet(df, year):
    '''Transform raw timesheet data frame to a data frame with a useful header, columns, and rows'''

    header = df.iloc[3]
    for i, head in enumerate(header):
        if head == 'Soma':
            last_index = i - 1
            break
    dates = header[5:last_index].apply(lambda x: x[:5].replace('/', '-') + '-' + year)
    header = header[:5].append(dates)
    df = df[4:][df.columns[:last_index]]
    df = df.rename(columns=header)
    df = df.drop(['Curso'], axis=1)
    df = df[df['Integrante'].notnull()]
    df.update(df[4:].fillna(0))
    return df

def read_timesheet(year_semester, path):
    '''Read the timesheet of year and semester in a Path
        Returns a dataframe.'''

    timesheet_file = pd.ExcelFile(path)
    raw_timesheet = pd.read_excel(timesheet_file, 'Timesheet ' + year_semester[:4] + '.' + year_semester[4])
    timesheet = clean_timesheet(raw_timesheet, year_semester[:4])
    return timesheet

def row_valid(project_name, activity_name, client_name, no_time_projects):
    '''Check if is a valid row based in project, activity and client.'''

    if project_name in no_time_projects:
        return True
    if 0 in (project_name, activity_name, client_name):
        return False
    return True

def fix_row(project_name, activity_name, client_name, no_time_projects):
    '''Returns project, activity and client name in a dict.'''

    names = {'project': project_name}
    if names['project'] in no_time_projects:
        names['projec'] = 'atividades gerais'
        names['client'] = 'no time'
        names['activity'] = names['project'].lower()
        return names    
    names['activity'] = activity_name.lower()
    names['client'] = client_name.lower()
    return names

def calculate_start_end(time, column):
    '''Receive time and the day 
        Returns the start and end in correct format.'''

    time_hours = (time * 50) // 60
    time_minutes = (time * 50) % 60
    start = datetime.strptime(column + 'T00:00:00-0300', "%d-%m-%YT%H:%M:%S%z")
    start = start - timedelta(days=1)
    end = start + timedelta(hours=time_hours, minutes=time_minutes)
    return (start, end)

def get_time(time):
    '''Returns a float that represents the time.'''

    if type(time) is str:
        try:
            time = float(time.replace('ha', '').replace(',', '.'))
        except:
            time = 0
    return time

def create_time_entries(time_entries, clean_timesheet):
    '''Returns a dataframe with all time entries in path file.'''

    timesheet_columns = list(clean_timesheet.iloc[:, 4:])
    for key, row in clean_timesheet.iterrows():
        member_acronym = row[0].lower()
        no_time_projects = ('Feriado', 'Falta justificada')
        if row_valid(row[1], row[2], row[3], no_time_projects):
            names = fix_row(row[1], row[2], row[3], no_time_projects)
            for column in timesheet_columns:
                time = get_time(row[column])
                if time > 0:
                    time_entry = {'member_acronym': member_acronym}
                    time_entry.update(fill_time_entry(column, names, time))
                    time_entries.append(time_entry, ignore_index=True)
    return time_entries        

def fill_time_entry(column, names, time):
    '''Fills all time entries in a timesheet row.
       Returns a dataframe with the timesheet added'''
    project_name = names['project']
    activity_name = names['activity']
    client_name = names['client']
    start, end = calculate_start_end(time, column)
    return {'project_name': project_name,
            'activity_name': activity_name,
            'client_name': client_name,
            'start': start, 'end': end}


def get_entity_id(entity, where, update=None):
    return globals().get(entity).update_or_create(where, update).id

def fill_ids(time_entries):
    '''Receives a data frame with all time entries without ids
        Returns a data frame with ids.'''

    member_ids=project_ids=activity_ids=client_ids={}
    members_acronym = time_entries.member_acronym.unique()
    project_names = time_entries.project_name.unique()
    activity_names = time_entries.activity_name.unique()
    client_names = time_entries.client_name.unique()
    zip_infos = zip(members_acronym, project_names, activity_names, client_names)
    for acronym, project_name, activity_name, client_name in zip_infos:
        if acronym is not None:
            email = {'email': acronym + "@certi.org.br"}
            member_ids[acronym] = get_entity_id('Member', {'acronym': acronym}, email)
        if project_name is not None:
            project_ids[project_name] = get_entity_id('Project', {'name': project_name})
        if activity_name is not None:
            activity_ids[activity_name] = get_entity_id('Activity', {'name': activity_name})
        if client_name is not None:
            client_ids[client_name] = get_entity_id('Client', {'name': client_name})

    time_entries_with_ids = update_time_entries_ids(time_entries, member_ids,
                                                    project_ids, activity_ids, client_ids)

    return time_entries_with_ids


def update_time_entries_ids(time_entries, member_ids, project_ids, activity_ids, client_ids):
    '''Receives a dataframe that represents the time_entries without the ids
        Returns with the correct ids, based on the dictionaries member_ids,
        project_ids, activity_ids and client_ids'''

    for index, row in time_entries.iterrows():
        time_entries.loc[index, 'member_id'] = member_ids[row[0]]
        time_entries.loc[index, 'project_id'] = project_ids[row[2]]
        time_entries.loc[index, 'activity_id'] = activity_ids[row[4]]
        time_entries.loc[index, 'client_id'] = client_ids[row[6]]
    return time_entries

def send_to_database(time_entries):
    '''Send time entries to database
       Return nothing.'''
    time_entries = time_entries.reset_index()
    for index in range(len(time_entries)):
        TimeEntry.update_or_create({
            "member_id": time_entries.loc[index, 'member_id'],
            "project_id": time_entries.loc[index, 'project_id'],
            "activity_id": time_entries.loc[index, 'activity_id'],
            "client_id": time_entries.loc[index, 'client_id'],
            "start": time_entries.loc[index, 'start'],
            "end": time_entries.loc[index, 'end']})

def import_timesheets():
    '''Function that creat a timesheet migration to neodata of a path.
        Returns nothing'''

    header_time_entries = {'member_acronym': '', 'member_id': '', 'project_name': '',
                          'project_id': '', 'activity_name': '', 'activity_id': '',
                          'client_name': '', 'client_id': '', 'start': '', 'end': ''}
    empty_time_entries = pd.DataFrame(columns=header_time_entries)

    timesheets_path = join(dirname(dirname(abspath(__file__))), 'old_timesheet_migration', 'timesheets')
    os.chdir(timesheets_path)

    for timesheet in glob.glob('*xlsx'):
        year_semester = timesheet.split('_')[3].split('.')[0][:5]
        path = timesheets_path + '\\' + timesheet
        clean_timesheet = read_timesheet(year_semester, path)
        time_entries = create_time_entries(empty_time_entries, clean_timesheet)
        time_entries_with_ids = fill_ids(time_entries)

        # Save time_entries in csv file at the same directory that has the timesheets
        time_entries_with_ids.to_csv(timesheets_path + '\\' + 'time_entries' + year_semester + '.csv')
        send_to_database(time_entries_with_ids)
        print("Done " + timesheet)
        time_entries = empty_time_entries

if __name__ == '__main__':
    import_timesheets()
