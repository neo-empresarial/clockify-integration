from orator import Model

class Member(Model):

    __table__ = "member"
    __fillable__ = ["clockify_id", "acronym", "email"]
    __primary_key__ = "clockify_id"
