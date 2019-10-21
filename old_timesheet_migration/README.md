# Migration from timesheets

Hey NEOson, this path was made to migrate all time entries from olds timesheets to NEOdata. The file **2017_timesheet_migration.py** was the first project ever made for this and it takes all time entries of the timesheets since 2017 to add in NEOdata. So, if you want to migrate time entries from another timesheet version, you have to check the **"How can I change the code to use in another timesheet?"** topic.

# How can I use?

Before you execute the file **2017_timesheet_migration.py** or similar, you have to make a path in your computer with all the timesheets since 2017, and make sure the timesheets are all in .xlsx file model. After that, you have to modify the line 214 of the code to the path you've chosen. 

The code was made to don't have troubles with duplicate information, because before send the data from database, it checks if already is there.

# How can I change the code to use in another timesheet? 

First of all you have to make sure that you're in a development environment, and to do so I recomend you to read project root README.md file.

After that I suggest you to understand what changed in the pattern of the timesheet from the version you're dealing with to the 2017.1 version. 

With that information in hands, you're going to modify the function **clean_timesheet** in line 9. This function crate a dataframe with the header equals the fourth line between second and "Soma" columns of the timesheet, adding the year in all dates. The funcion also get the data from information below the header, filling the empty values with 0.

If you want to test any changes you made in the code, it's **important to comment the returns of the function send_to_neodata(timeentrys)** in line 248. When you run this code, a .csv file should be created for each timesheet. It's important for you to check if this data is correct, before sending it to the production database.