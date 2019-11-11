# Migration from timesheets

Hey NEOson, here you will find the tools to migrate all time entries from olds timesheets to NEOdata. The script in **timesheet_migration.py** takes all time entries of the timesheets from a timesheets folder to add in NEOdata. It's important to stress that this program was used to migrate time entries from as far as 2017, for before that we only filled the timesheet with data that was within regular business hours.

So, as timesheets have the time that the person works in a week and NEOdata should receive start and end about a time entry, we make the program to send the time entries start in the Sunday 00:00 of each week.

# How can I use it?

Before you execute the file **timesheet_migration.py** or similar, you have to save all timesheets that you want to get information in the timesheets folder. It's important to know that the program iterate for all .xlsx files that have in the folder, so make sure that the timesheets are the only Excel files in this path.

Another information that it's important to know is the database itself. Before you execute the script you have to make sure that all strings are in lower case and column activity_id in TimeEntry table accept Null values. 

You don't need to worry about duplicate values if you run the code twice because before sending the data to the database, it checks if it is already there.

# How can I change the code to use in another timesheet? 

First of all, you have to make sure that you're in a development environment and to do so I recommend you to read project root README.md file.

After that, I suggest you understand what changed in the pattern of the timesheet from the version you're dealing with to the 2017.1 version.

With that information in hands, you're going to modify the function **clean_timesheet**(line 12) and **read_timesheet**(line 29). The first function create a dataframe with the header equals the fourth line oh the timesheet, adding the year on all dates. The function also gets the data from the information below the header, filling the empty values with 0. The second function read the table in an Excel file, based on the pattern name of the timesheet and table.

If you want to test any changes you made in the code, it's **important to comment on the returns of the function send_to_neodata(time entry)** inline 248. When you run this code, a .csv file should be created for each timesheet. You need to check if this data is correct, before sending it to the production database.