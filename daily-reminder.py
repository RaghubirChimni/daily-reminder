import os
from datetime import datetime, date
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import calendar

client = Client(
    os.environ['TWILIO_ACCOUNT_SID'],
    os.environ['TWILIO_AUTH_TOKEN']
)

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
        f"Today is {today_str}.\n\n"
        f"{percentage}% of the year has passed.\n\n"
        f"Make today count! 💪"
    )

    recipient_numbers = [number.strip() for number in os.environ['RECIPIENT_PHONE_NUMBERS'].split(',')]
    for recipient_number in recipient_numbers:
        try:
            result = client.messages.create(
                body=message,
                from_=os.environ['TWILIO_PHONE_NUMBER'],
                to=recipient_number.strip()
            )
            print(f"SMS sent successfully!")
        except TwilioRestException as e:
            print(f"Error sending SMS | status: {e.status} | code: {e.code} | code link: https://www.twilio.com/docs/errors/{e.code}")

if __name__ == "__main__":
    send_reminder()