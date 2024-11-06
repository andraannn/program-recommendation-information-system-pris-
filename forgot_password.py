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
          background-color: #a41d21;
          border: none;
          color: #ffffff !important; 
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          cursor: pointer;
          border-radius: 12px;
          padding: 10px 24px;
        }}
        .card {{
          margin: 0 auto;
          width: 600px;
          background: #f4f3e3;
          border-radius: 10px;
          box-shadow: 10px 10px 10px 10px rgba(0, 0, 0, 0.05);
          box-sizing: border-box;
        }}
         .image-container {{
          text-align: center;
        }}
        .image-container img {{
          width: 100px;
          border-radius: 10px 10px 0 0;
        }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="image-container" style="padding-top: 20px;">
          <img src="https://www.msuiit.edu.ph/assets/img/seal-02.png" style="max-width: 100%; border-radius: 10px 10px 0 0;" alt="Image"> 
        </div>
        <div style="padding: 20px;">
          <p style="text-align: center; font-family: 'Poppins', sans-serif; font-weight: 500; font-size: 18px; line-height: 1.5;">You have requested to reset your account password.</p>
          <p style="text-align: center; font-family: 'Poppins', sans-serif; font-weight: 500; font-size: 18px; line-height: 1.5;">Please click the button below to reset your account password:</p>
          <a href="{reset_link}" class="button" style="display: block; margin: 0 auto;">Reset Password</a>
          <br><br>
          <p>If the button above does not work, you can also click the link below:</p>
          <p><a href="{reset_link}">{reset_link}</a></p>
        </div>
      </div>
    </body>
    </html>
    """

    msg = Message("PRIS Reset Password Request", recipients=[email])
    msg.body = message
    msg.html = message  # Use the HTML version for better formatting
    mail.send(msg)
    
