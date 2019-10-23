# Migration from timesheets

Hey NEOson, this path was made to migrate all time entries from olds timesheets to NEOdata. The file **timesheet_migration.py** was the first project ever made for this and it takes all time entries of the timesheets from a timesheets folder to add in NEOdata. It's important to say that program was used to migrate time entries since 2017, because before that the members of NEO just fill the timesheet with the regular business hours.

So, as timesheets has the time that the person work in a week and NEOdata should receive start and end about a time entry, we make the program to send the time entries start in the Sunday 00:00 of each week.

# How can I use?

Before you execute the file **timesheet_migration.py** or similar, you have to save all timesheets that you want to get information in the timesheets folder. It's important to know that the program iterate for all .xlsx files that has in the folder, so make sure that the timesheets are the only Excel files in this path.

The code was made to don't have troubles with duplicate information, because before send the data to database, it checks if already is there.

# How can I change the code to use in another timesheet? 

First of all you have to make sure that you're in a development environment, and to do so I recomend you to read project root README.md file.

After that I suggest you to understand what changed in the pattern of the timesheet from the version you're dealing with to the 2017.1 version.

With that information in hands, you're going to modify the function **clean_timesheet**(line 12) and **read_**(line 30). The first function crate a dataframe with the header equals the fourth line between second and "Soma" columns of the timesheet, adding the year in all dates. The funcion also get the data from information below the header, filling the empty values with 0. The second function read the table in Excel file, based in the pattern name of the timesheet and table.

If you want to test any changes you made in the code, it's **important to comment the returns of the function send_to_neodata(timeentrys)** in line 248. When you run this code, a .csv file should be created for each timesheet. It's important for you to check if this data is correct, before sending it to the production database.