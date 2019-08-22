from orator import Model

class Client(Model):

    __table__ = "client"
    __fillable__ = ["clockify_id", "name"]
    __primary_key__ = "clockify_id"
