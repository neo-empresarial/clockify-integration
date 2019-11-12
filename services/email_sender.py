from sendgrid.helpers.mail import Email, Mail
from sendgrid import SendGridAPIClient
import os


class EmailSender:
    def __init__(self, emails):
        self.sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        self.recipients = emails

    def send(self):
        from_email = Email("data@neo.ufsc.br", "NEO-Data mailer")
        to_emails = self.recipients
        subject = "(Scheduled) NEO Data has just been updated."
        mail = Mail(
            from_email,
            to_emails,
            subject,
            html_content="<strong>Our lambda functions are born and say hello</strong>",
        )
        return self.sg.client.mail.send.post(request_body=mail.get())
