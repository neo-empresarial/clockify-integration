import os
import pandas as pd
#import dateutil.parser as parser
# from __somewherewedunno__ import TimeEntry

def calculate_end(row):
    minutes = []
    for time in row[4:]:
        minutes = time * 50

    print(minutes)
    return 0
    '''end_hour = minutes / 60
    end_minutes = minutes % 60
    end = str(end_hour)+ ':' + str(end_minutes)
'''

def clean_df(df, year):

    header = df.iloc[3]
    header = header[:5].append(header[5:-1].apply(lambda x: x[:5].replace('/','-') + '-' + year))
    df = df[4:]
    df = df.rename(columns = header) 
    df = df.drop(['Curso'], axis=1)
    df = df[df['Integrante'].notnull()]
    df = df[df.columns[:-1]]
    df.update(df.fillna(0))
    return df



#starts the code
df = pd.read_excel(r'D:\Desktop\UFSC\Monitoramento_de_horas_20191.xlsx')
df = clean_df(df, '2019')
print(df)
'''
for row in df.itertuples(index=False):
    # TimeEntry.create({
    #     "member_id": Member.first_or_create(acronym=row[0]).id,
    #     "project_id": Project.first_or_create(name=row[1]).id,
    #     "activity_id": Activity.first_or_create(name=row[2]).id,
    #     "client_id": Client.first_or_create(name=row[3]).id,
    #     "start": parser.parse(df.columns[4]),  # colocaremos no domingo
    #     "end": end
    #     })
    pass
'''