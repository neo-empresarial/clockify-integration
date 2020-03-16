from models import *
from orator.orm import belongs_to


class IndicatorConsolidation(Model):
    __table__ = "indicator_consolidation"
    __fillable__ = [
        "value",
        "start_date",
        "end_date",
        "member_id",
        "indicator_id",
        "created_at",
        "updated_at",
    ]
    __primary_key__ = "id"

    @belongs_to("member_id", "id")
    def member(self):
        return Member

    @belongs_to("indicator_id", "id")
    def indicator(self):
        return Indicator
