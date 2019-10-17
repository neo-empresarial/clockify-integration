from datetime import datetime, timedelta
from config import settings
from models import Activity, Client, Member, Project, TimeEntry
import os
import glob
import pandas as pd
#import dateutil.parser as parser


'''---------------Periferic Funcions.--------------------'''
def clean_timesheet(df, year):
    '''Clean the timesheet of the year.'''

    header = df.iloc[3]
    for i, head in enumerate(header):
        if head == 'Soma':
            last_index = i - 1
            break
    dates = header[5:last_index].apply(lambda x: x[:5].replace('/','-') + '-' + year)
    header = header[:5].append(dates)
    df = df[4:][df.columns[:last_index]]
    df = df.rename(columns = header)
    df = df.drop(['Curso'], axis=1)
    df = df[df['Integrante'].notnull()]
    df.update(df.fillna(0))
    return df

def update_time_entry(time_entry, semester, path):
    '''Receive the Time Entry to update with the 
    values of the timesheet in path of the year.'''

    xlsx = pd.ExcelFile(path)
    timesheet = pd.read_excel(xlsx, 'Timesheet ' + semester[:4] + '.' + semester[4])
    timesheet = clean_timesheet(timesheet, semester[:4])
    timesheet_collumns = list(timesheet.iloc[:, 4:])

    for key, row in timesheet.iterrows():
        member_acronym = row[0].lower()
        project_name = 0 
        activity_name = 0
        client_name = 0

        if (row[1] == 'Feriado' or row[1] == 'Falta justificada'):
            project_name = row[1].lower()
            activity_name = ''
            client_name = 'no time'

        elif row[1] != 0:
            project_name = row[1].lower()

            if row[2] != 0:
                activity_name = row[2].lower()

                if row[3] != 0:
                    client_name = row[3].lower()

        if (client_name == 0 or activity_name == 0 or project_name == 0):
            time_entry.drop(key, inplace=True)
        
        else:
            for column in timesheet_collumns:

                if type(row[column]) is str:
                    try:
                        time = float(row[column].replace('ha','').replace(',', '.'))
                    except:
                        time = 0
                else:
                    time = row[column]

                if activity_name == 0:
                    activity_name = ""

                if time > 0:
                    time_hours = (time * 50) // 60
                    time_minutes = (time * 50) % 60
                    start = datetime.strptime(column + 'T00:00:00-0300', "%d-%m-%YT%H:%M:%S%z")-timedelta(days = 1)
                    end = start+timedelta(hours=time_hours, minutes=time_minutes)

                    time_entry = time_entry.append({'member_acronym': member_acronym,
                                                'project_name': project_name,
                                                'activity_name': activity_name,
                                                'client_name': client_name,
                                                'start': start, 'end': end}, ignore_index=True)
    
    return time_entry

def get_member_id(acronym):
    try:
        member_id = Member.where("acronym", acronym).first().id

    except:
        email = acronym + "@certi.org.br"
        Member.update_or_create({"acronym": acronym},
                                {"email": email})
        member_id = Member.where("acronym", acronym).first().id

    return member_id

def get_project_id(name):
    try:
        project_id = Project.where("name", name).first().id

    except:
        Project.update_or_create({"name": name})
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
        Client.update_or_create({"name": name})
        client_id = Client.where("name", name).first().id

    return client_id

def update_time_entry_ids(time_entry, member_ids, project_ids, activity_ids, client_ids):
    '''Receives the time_entry without the ids 
        and return with tue correct ids,
        based on the dictionarys member_ids,
        project_ids, activity_ids and client_ids'''

    for index, row in time_entry.iterrows():
        for member_acronym, member_id  in member_ids.items():
            if member_acronym == row[0]:
                time_entry.loc[index, 'member_id'] = member_id
                break

        for project_name, project_id  in project_ids.items():
            if project_name == row[2]:
                time_entry.loc[index, 'project_id'] = project_id
                break

        for activity_name, activity_id  in activity_ids.items():
            if activity_name == row[4]:
                time_entry.loc[index, 'activity_id'] = activity_id
                break

        for client_name, client_id  in client_ids.items():
            if client_name == row[6]:
                time_entry.loc[index, 'client_id'] = client_id
                break

    return time_entry

def send_to_neodata(time_entry):
    time_entry = time_entry.reset_index()
    for index in range(len(time_entry)):
        print(time_entry.loc[index])
        TimeEntry.update_or_create({
         "member_id": time_entry.loc[index, 'member_id'],
         "project_id": time_entry.loc[index, 'project_id'],
         "activity_id": time_entry.loc[index, 'activity_id'],
         "client_id": time_entry.loc[index, 'client_id'],
         "start": time_entry.loc[index, 'start'],
         "end": time_entry.loc[index, 'end']
         })

'''-----------------------Main Function---------------------------------'''
def import_timesheets():
    '''Function that creat a timesheet migration to neodata of a path.
    '''
    header_time_entry = {'member_acronym': '', 'member_id': '', 'project_name': '',
                     'project_id': '', 'activity_name': '','activity_id': '',
                     'client_name': '', 'client_id': '', 'start': '', 'end': ''}

    empty_time_entry = pd.DataFrame(columns=header_time_entry)
    
    timesheets_directory = r'D:\Desktop\UFSC\NEO\MPG_Desafio\timesheets' #Path in the computer that has all the Timesheets
    os.chdir(timesheets_directory)
    for timesheet in glob.glob('*xlsx'):
        semester = timesheet.split('_')[3].split('.')[0][:5]
        path = timesheets_directory + '\\' + timesheet
        time_entry = update_time_entry(empty_time_entry, semester, path)
    
        member_ids = {}
        members_acronym = time_entry.member_acronym.unique()
        for acronym in members_acronym:
            member_ids[acronym] = get_member_id(acronym)

        project_ids = {}
        project_names = time_entry.project_name.unique()
        for name in project_names:
            project_ids[name] = get_project_id(name)
        
        activity_ids = {}
        activity_names = time_entry.activity_name.unique()
        for name in activity_names:
            activity_ids[name] = get_activity_id(name)
        
        client_ids = {}
        client_names = time_entry.client_name.unique()
        for name in client_names:
            client_ids[name] = get_client_id(name)
        
        time_entry = update_time_entry_ids(time_entry, member_ids,
                                        project_ids, activity_ids, client_ids)
    
        #Save time_entry in csv file in the same directory that is the timesheets
        #time_entry.to_csv(timesheets_directory + '\\' + 'time_entry' + semester + '.csv')
        
        send_to_neodata(time_entry)
        print("Done " + timesheet)
        time_entry = empty_time_entry

if __name__ == '__main__':
    import_timesheets()
    