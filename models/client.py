from orator import Model

class Client(Model):

    __table__ = 'Clients'
    __fillable__ = ['name', 'clockifyId']