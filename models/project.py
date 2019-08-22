from orator import Model

class Project(Model):

    __table__ = "project"
    __fillable__ = ["clockify_id", "name"]
    __primary_key__ = "clockify_id"
