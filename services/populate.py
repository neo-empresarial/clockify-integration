import sys
sys.path.append('../')
from config import settings
from models import Activity, Client, Member, Project, TimeEntry

if __name__ == "__main__":
    Member.save_from_clockify()
    Project.save_from_clockify()
    Activity.save_from_clockify()
    Client.save_from_clockify()
    TimeEntry.save_from_clockify()
