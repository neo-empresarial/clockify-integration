from orator import Model

class Project(Model):

    __table__ = "projects"
    __fillable__ = ["name", "clockify_id"]