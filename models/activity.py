from orator import Model

class Activity(Model):

    __table__ = "activity"
    __fillable__ = ["name"]
    __primary_key__ = "id"
