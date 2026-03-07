import os
from datetime import datetime, date
import calendar
import resend

resend.api_key = os.environ['RESEND_API_KEY']

def get_year_progress():
    today = datetime.now().date()
    end_of_year = date(today.year, 12, 31)

    days_passed = (today - date(today.year, 1, 1)).days
    total_days = 366 if calendar.isleap(today.year) else 365
    percentage = round((days_passed / total_days) * 100, 1)

    return percentage

def send_reminder():
    percentage = get_year_progress()
    today_str = datetime.now().strftime('%A, %B %d, %Y')
    
    message = (
        f"Today is {today_str}.<br><br>"
        f"{percentage}% of the year has passed.<br><br>"
        f"Make today count! 💪"
    )
    
    recipient_emails = [email.strip() for email in os.environ['RECIPIENT_EMAILS'].split(',')]
    
    for recipient_email in recipient_emails:
        try:
            resend.Emails.send({
                "from" : "noreply@raghubirchimni.com",
                "to": recipient_email,
                "subject": f"Daily Reminder: {today_str}",
                "html": f"<pre>{message}</pre>"
            })
            print(f"Email sent successfully")
        except Exception as e:
            print(f"Error sending email to {recipient_email}: {e}")

if __name__ == "__main__":
    send_reminder()