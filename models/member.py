from orator import Model

class Member(Model):

    __table__ = "members"
    __fillable__ = ["acronym", "clockify_id", "email"]