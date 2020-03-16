from models import *


class Indicator(Model):

    __table__ = "indicator"
    __fillable__ = ["name", "frequency"]
    __primary_key__ = "id"
    __incrementing__ = True
