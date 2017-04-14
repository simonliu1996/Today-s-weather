#This project aims to send me an email of weather everyday
import datetime
import smtplib
import requests
#import simplejson as json
import json
from email.mime.text import MIMEText
from config import mail_settings, send_to_addresses, api_key
 
def fetch_forecast(api_key, request_type):
    mail_url = 'http://api.wunderground.com/api/' + api_key + '/' + request_type +'/forecast/q/VA/Leesburg.json'
    r = requests.get(mail_url)
    j = json.loads(r.text)
    return j
 
def build_html(forecast_json):
    # build some HTML snippets to open and close this email
    html_open = """\
    <html>
      <head></head>
      <body>
    """
    html_close = """\
      </body>
    </html>
    """
 
    # let's now build the HTML body contents
    wxdate = forecast_json['forecast']['txt_forecast']['date']
    mail_text = '<h3>Hello, MR.Liu and MRs.Chu!</h3><p>Here is the Ann Arbor, MI., weather forecast as of ' + wxdate + '</p>'
    forecast_length = len(forecast_json['forecast']['txt_forecast']['forecastday']) - 1
 
    # looping through the JSON object
    for i in range(0, forecast_length):
        cast = '<p><b>' + forecast_json['forecast']['txt_forecast']['forecastday'][i]['title'] + '</b>: ' +\
               forecast_json['forecast']['txt_forecast']['forecastday'][i]['fcttext'] + '</p>'
        mail_text += cast
 
    # put it all together
    html_body = html_open + mail_text + html_close
    return html_body
 
def send_email(mail_text):
    # Set the current time and add that to the message subject
    cur_date = datetime.date.today().strftime("%B") +\
        ' ' + datetime.date.today().strftime("%d") +\
        ', ' + datetime.date.today().strftime("%Y")
    subject = 'Weather forecast for ' + cur_date
 
    # Set up the message subject, etc. Then send it.
    COMMASPACE = ', '
 
    msg = MIMEText(mail_text, 'html')
    msg['Subject'] = subject
    msg['From'] = mail_settings['from']
    msg['To'] = COMMASPACE.join(send_to_addresses)
 
    server = smtplib.SMTP(mail_settings['smtp'], 25)
    server.login(mail_settings['address'], mail_settings['pw'])
    server.set_debuglevel(1)
    server.sendmail(mail_settings['address'], send_to_addresses, msg.as_string())
    server.quit()
 
if __name__ == "__main__":
    forecast_json = fetch_forecast(api_key, 'forecast')
    mail_text = build_html(forecast_json)
    send_email(mail_text)