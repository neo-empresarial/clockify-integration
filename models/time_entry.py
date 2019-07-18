from orator import Model
from orator.orm import has_one
from models import Activity

class TimeEntry(Model):

    __table__ = "time_entries"
    __fillable__ = ["id" ,"start" ,"end" ,"description" ,"activity_id" ,"project_id" ,"member_id" ,"client_id" ,"created_at" ,"updated_at" ,"clockify_id" ,"duration"]

