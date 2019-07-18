from orator import Model

class Activity(Model):

    __table__ = 'Activities'
    __fillable__ = ['name']