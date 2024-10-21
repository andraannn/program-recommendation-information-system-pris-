from flask import url_for
from flask_mail import Message
from mail import mail

# Helper function to send password reset email
def send_password_reset_email(email, reset_token):
    reset_link = url_for('reset_password', token=reset_token, _external=True)
    
    
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
      
      <p>You have requested to reset your account password.</p>
      <p>Please click the button below to reset your account password:</p>
      <a href="{reset_link}" class="button">Reset Password</a>
      <br><br>
      <p>If the button above does not work, you can also click the link below:</p>
      <p><a href="{reset_link}">{reset_link}</a></p>
      
    </body>
    </html>
    """

    msg = Message("CRIS Reset Password Request", recipients=[email])
    msg.body = message
    msg.html = message  # Use the HTML version for better formatting
    mail.send(msg)
    
