from orator import Model

class Activity(Model):

    __table__ = "activities"
    __fillable__ = ["name"]