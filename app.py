from flask import Flask, request, render_template,  redirect, url_for, send_from_directory, jsonify
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
import requests


#new
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)

# app.config['MAIL_SERVER'] = 'smtp.office365.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# # app.config['MAIL_RECIEVER'] = os.getenv('MAIL_RECIEVER')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

#new
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = os.getenv("SMTP_PORT", 587)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

mail = Mail(app)

@app.route('/')
def index():
    return 'live'

#new
def send_email(to_address, subject, message):
   

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain" ))

        # Establish a secure session with the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Use TLS encryption
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to_address, msg.as_string())

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


@app.route("/submit-form", methods=["POST"])
def send_email_route():


    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    request_type = request.form.get('request')
    body = request.form.get('message')
    recaptcha = request.form.get('g-recaptcha-response')

#captcha verification with Google
    if not recaptcha:
        return jsonify({"success": False, "message": "reCAPTCHA response is missing!"})

    # Verify reCAPTCHA with Google
    verification_url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": recaptcha
    }

    response = requests.post(verification_url, data=data)
    result = response.json()

    if result.get("success"):
        to_address = "dpo@privacycure.com"
        subject = "new client message"
        message = f'''Good day team,\n\nThere is a new message from a client: 
        Name: {name}
        Email: {email}
        Phone: {phone}
        Request Type: {request_type}
        \n\n{body} 
        \n\nRegards'''

        if send_email(to_address, subject, message):
            return '<div style="text-align: center; margin-top:20vh; font-size:20px;">Thank you for you submission!, We will get back to you soon <div> To go home: <a href="https://privacycure.com">click here!!</a> </div></div>'
        else:
            return '<div style="text-align: center; margin-top:20vh; font-size:20px;">Unfortunately there has been an error processing your message. <div> To go home: <a href="https://privacycure.com">click here!!</a> </div></div>'
    
    else:
        return "Suspicious Activity Detected"

    

# @app.route('/submit-form', methods=['POST'])
# def submit_form():
    
#     name = request.form.get('name')
#     email = request.form.get('email')
#     phone = request.form.get('phone')
#     request_type = request.form.get('request')
#     message = request.form.get('message')

#     subject = 'New client message'
#     message_body = message

#     msg = Message(subject = subject,
#                   sender = app.config['MAIL_USERNAME'],
#                 #   recipients = ['dpo@privacycure.com']
#                   recipients = ['dpo@privacycure.com']
#                   ) 
#     msg.body = f'''Good day team,\n\nThere is a new message from a client: 
#     Name: {name}
#     Email: {email}
#     Phone: {phone}
#     Request: {request_type}
#     \n\n{message_body} 
#     \n\nRegards'''


#     # print( app.config['MAIL_USERNAME'] )

#     try:
#         # mail.connect()
#         mail.send(msg)
#         return '<div style="text-align: center; margin-top:20vh; font-size:20px;">Thank you for you submission!, We will get back to you soon <div> To go home: <a href="https://privacycure.com">click here!!</a> </div></div>'
#         # return 'Email sent successfully!'
#     except Exception as e:
#         return f'Failed to send email: {e}'

if __name__ == '__main__':
    app.run(debug=True)
