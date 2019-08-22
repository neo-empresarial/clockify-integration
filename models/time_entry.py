from orator import Model
from orator.orm import belongs_to
from models import Activity, Client, Member, Project
from orator.orm import belongs_to

class TimeEntry(Model):

    __table__ = "time_entry"
    __fillable__ = ["clockify_id", "member_id", "project_id", "activity_id", "client_id", "start", "end", "description", "created_at", "updated_at"]
    __primary_key__ = "clockify_id"

    @belongs_to('member_id', 'clockify_id')
    def member(self):
        return Member

    @belongs_to('project_id', 'clockify_id')
    def project(self):
        return Project

    @belongs_to('activity_id', 'id')
    def activity(self):
        return Activity
    
    @belongs_to('client_id', 'clockify_id')
    def client(self):
        return Client
