from orator import Model
from orator.orm import has_one
from models import Activity

class TimeEntry(Model):

    __table__ = 'TimeEntries'
    __fillable__ = ['start', 'end', 'description', 'duration', 'clockifyId']

    @has_one
    def activityId(self):
        return Activity
    #tem uma atividade
    #modelamos errado?
    #tem um project
    #tem um member
    #tem um client