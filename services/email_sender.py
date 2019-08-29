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
