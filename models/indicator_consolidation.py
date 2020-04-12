from models import *
from orator.orm import belongs_to
from datetime import datetime, timedelta, time


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

    @staticmethod
    def calculate_prep(start, end, member, neo_id=None):
        if neo_id is None:
            neo_id = Client.where("name", "neo").first().id
        if member.date_deactivated is not None:
            if start >= member.date_deactivated:
                return None
        time_entries = (
            TimeEntry.where("member_id", member.id)
            .where("client_id", "!=", neo_id)
            .where("start", ">=", start)
            .where("start", "<=", end)
            .get()
        )
        total_seconds = time_entries.sum(lambda te: (te.end - te.start).total_seconds())
        if total_seconds is None:
            value = 0
        else:
            value = total_seconds / (20 * 50 * 60)
        return value

    @staticmethod
    def get_first_sunday(start):
        if start.isoweekday != 7:
            start = start - timedelta(days=start.isoweekday())
        if (datetime.now() - start).days < 7:
            start = start - timedelta(days=7)
        return datetime.combine(start, time())

    @staticmethod
    def get_last_saturday():
        now = datetime.now()
        week_day = now.isoweekday()
        if week_day == 7:
            saturday = now - timedelta(days=1)
        elif week_day != 6:
            saturday = now - timedelta(days=week_day + 1)
        else:
            saturday = now
        return saturday

    @staticmethod
    def daterange(start, end):
        for days in range(0, int((end - start).days) + 1, 7):
            yield {
                "start": start + timedelta(days=days),
                "end": start
                + timedelta(days=days + 6, hours=23, minutes=59, seconds=59),
            }

    @classmethod
    def get_time_intervals(cls, start, frequency):
        if not isinstance(start, datetime):
            start = datetime.fromisoformat(start)
        if frequency == "weekly":
            first_sunday = cls.get_first_sunday(start)
            last_saturday = cls.get_last_saturday()
            return cls.daterange(first_sunday, last_saturday)

    @classmethod
    def populate_prep(cls, start):
        prep = Indicator.where("name", "prep").first()
        intervals = cls.get_time_intervals(start, prep.frequency)
        neo_id = Client.where("name", "neo").first().id
        db.update("SET timezone='America/Sao_Paulo';")
        for interval in intervals:
            for member in Member.all():
                value = cls.calculate_prep(
                    interval["start"], interval["end"], member, neo_id
                )
                if value is not None:
                    IndicatorConsolidation.update_or_create(
                        {
                            "start_date": interval["start"],
                            "end_date": interval["end"],
                            "member_id": member.id,
                            "indicator_id": prep.id,
                        },
                        {"value": value, "updated_at": datetime.now()},
                    )
        db.update("SET timezone='UTC';")
