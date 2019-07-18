from orator import Model

class Project(Model):

    __table__ = "Projects"
    __fillable__ = ["name", "clockifyId"]