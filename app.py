from flask import Flask, request, render_template,  redirect, url_for, send_from_directory
import os
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='')

mail = Mail(app)

@app.route('/')
def index():
    return 'live'
    

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    request_type = request.form.get('request')
    message = request.form.get('message')
    
    # For demonstration, let's print the data to the console
    # print(f'Name: {name}, Email: {email}, Phone: {phone}, Request: {request_type}  Message: {message}')

    # mail = Mail(app)

    subject = 'New client message'
    message_body = message

    msg = Message(subject = subject,
                  sender = MAIL_USERNAME,
                  recipients = MAIL_RECIEVER) # Send to this email address
    msg.body = f'''Good day team,\n\nThere is a new message from a client: 
    Name: {name}
    Email: {email}
    Phone: {phone}
    Request: {request_type}
    \n\n{message_body} 
    \n\nRegards'''

    try:
        # mail.connect()
        mail.send(msg)
        return '<div style="text-align: center; margin-top:20vh; font-size:20px;">Thank you for you submission!, We will get back to you soon <div> To go home: <a href="https://privacycure.com">click here!!</a> </div></div>'
        # return 'Email sent successfully!'
    except Exception as e:
        return f'Failed to send email: {e}'

    # Redirect or show a success page after form submission
    return '<div style="text-align: center; margin-top:20vh; font-size:20px;">Thank you for you submission!, We will get back to you soon <div> To go home: <a href="https://privacycure.com">click here!!</a> </div></div>'


if __name__ == '__main__':
    app.run(debug=True)
