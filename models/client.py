from orator import Model

class Client(Model):

    __table__ = "clients"
    __fillable__ = ["name", "clockify_id"]