from orator import Model

class Member(Model):

    __table__ = 'Members'
    __fillable__ = ['acronym', 'clockifyId', 'email']