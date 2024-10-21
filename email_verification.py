from flask import url_for
from flask_mail import Message
from mail import mail  # Import mail from the new module

def send_verification_email(email, verification_token):
    verification_link = url_for('verify_email', token=verification_token, _external=True)
    message = f"""
    <html>
    <head>
      <style>
        .button {{
          background-color: #b4d4fa;
          border: none;
          color: #000000; 
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          cursor: pointer;
          border-radius: 12px;
          padding: 10px 24px;
        }}
      </style>
    </head>
    <body>
 
      <p>You have successfully created an account.</p>
      <p>Please click the button below to verify your email:</p>
      <a href="{verification_link}" class="button">Verify Email</a>
      <br><br>
      <p>If the button above does not work, you can also click the link below:</p>
      <p><a href="{verification_link}">{verification_link}</a></p>
      
    </body>
    </html>
    """

    msg = Message("CRIS Registration Email Verification", recipients=[email])
    msg.body = message
    msg.html = message  # Use the HTML version for better formatting
    mail.send(msg)
