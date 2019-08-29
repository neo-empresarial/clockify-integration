from chalice import Chalice, Rate

app = Chalice(app_name="neo-clockify-data")

import os
import sendgrid
from sendgrid.helpers.mail import Email, Mail

class EmailSender:
    def __init__(self, emails):
        self.sg = sendgrid.SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        self.recipients = emails

    def send(self):
        from_email = Email(
            "data@neo.ufsc.br", "NEO-Data mailer")
        to_emails = self.recipients
        subject = "(Scheduled) Hello from NEO-Data @JNR @LAB"
        mail = Mail(from_email, to_emails, subject, html_content='<strong>Our lambda functions are born and say hello</strong>')
        response = self.sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

# Automatically runs every 5 minutes
@app.schedule(Rate(1, unit=Rate.MINUTES))
def periodic_task(event):
    EmailSender(['lab@certi.org.br', 'jnr@certi.org.br']).send()
    print('Ok.')

# def update_time_entries(request):
#     return f"Hello World!"

# def update_users(request):
#     return f"Hello World!"


# def update_projects(request):
#     return f"Hello World!"


# def update_activities(request):
#     return f"Hello World!"


# def update_tags(request):
#     return f"Hello World!"
