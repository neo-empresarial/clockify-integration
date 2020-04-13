try:
  import unzip_requirements
except ImportError:
  pass
import json
import datetime
from models import *

def update(event, context):
    now = datetime.datetime.now()
    three_weeks_ago = now - datetime.timedelta(weeks=3)

    Member.save_from_clockify()
    Client.save_from_clockify()
    Project.save_from_clockify()
    Activity.save_from_clockify()
    TimeEntry.save_from_clockify(start=three_weeks_ago.strftime('%Y-%m-%dT%H:%M:%SZ'))
    IndicatorConsolidation.populate_prep(start=three_weeks_ago.strftime('%Y-%m-%dT%H:%M:%S'))
    
    return {
        "message": "Function executed successfully!",
        "event": event
    }
