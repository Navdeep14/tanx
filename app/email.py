# app/email.py
import smtplib
from email.mime.text import MIMEText
from . import db
from .models import Alert
import requests

def send_email(alert):
    msg = MIMEText(f'Target price reached for {alert.cryptocurrency}! Current price: ${get_current_price(alert.cryptocurrency)}')
    msg['Subject'] = 'Price Alert Triggered'
    msg['From'] = 'xyz@gmail.com'
    msg['To'] = 'abcd@example.com'

    try:
    # Send email using Gmail SMTP (you may need to enable "Less secure app access" in your Gmail settings)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('xx@gmail.com', 'yy@1234')
            server.sendmail('xx@gmail.com', 'abcd@example.com', msg.as_string())
    except Exception as e:
        raise 'there is problem sending mail to user'

    # Update alert status to 'triggered'
    alert.status = 'triggered'
    db.session.commit()

def get_current_price(cryptocurrency):
    try:
        key = "https://api.binance.com/api/v3/ticker/price?symbol={}".format(cryptocurrency)
        # requesting data from url 
        data = requests.get(key)   
        data = data.json() 
        print(f"{data['symbol']} price is {data['price']}")
        return data['price']
    except Exception as e:
        raise "Exception occured {}".format(e)
