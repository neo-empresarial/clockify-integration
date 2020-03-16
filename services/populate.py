import sys

sys.path.append("../")
from models import Activity, Client, Member, Project, TimeEntry

if __name__ == "__main__":
    Member.save_from_clockify()
    Client.save_from_clockify()
    Project.save_from_clockify(archived="")
    Activity.save_from_clockify()
    TimeEntry.save_from_clockify(start="2020-03-01T00:00:01Z")
