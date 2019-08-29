from chalice import Chalice, Rate

app = Chalice(app_name="neo-clockify-data")

import os
import sendgrid
from sendgrid.helpers.mail import Email, Mail

class EmailSender:
    def __init__(self, recipients):
        self.sg = sendgrid.SendGridAPIClient(
            apikey=os.environ.get("SENDGRID_API_KEY"))
        self.recipients = recipients

    def send(self):
        from_email = Email(
            "data@neo.ufsc.br", "NEO-Data mailer")
        to_emails = self.recipients
        subject = "(Scheduled) Hello from NEO-Data @JNR @LAB"
        mail = Mail(from_email, subject, to_emails, html_content='<strong>Our lambda functions are born and say hello</strong>')
        self.sg.client.mail.send.post(request_body=mail.get())

# Automatically runs every 5 minutes
@app.schedule(Rate(1, unit=Rate.DAYS))
def periodic_task(event):
    EmailSender.send(['jnr@certi.org.br', 'lab@certi.org.br'])
    return 'Ok.'
    
def update_time_entries(request):
    return f"Hello World!"

def update_users(request):
    return f"Hello World!"


def update_projects(request):
    return f"Hello World!"


def update_activities(request):
    return f"Hello World!"


def update_tags(request):
    return f"Hello World!"
