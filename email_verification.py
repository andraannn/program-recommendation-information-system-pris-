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
          <p style="text-align: center; font-family: 'Poppins', sans-serif; font-weight: 500; font-size: 18px; line-height: 1.5;">You have successfully created an account.</p>
          <p style="text-align: center; font-family: 'Poppins', sans-serif; font-weight: 500; font-size: 18px; line-height: 1.5;">Please click the button below to verify your email:</p>
          <a href="{verification_link}" class="button" style="display: block; margin: 0 auto;">Verify Email</a>
          <br><br>
          <p>If the button above does not work, you can also click the link below:</p>
          <p><a href="{verification_link}">{verification_link}</a></p>
        </div>
      </div>
    </body>
    </html>
    """

    msg = Message("PRIS Registration Email Verification", recipients=[email])
    msg.body = message
    msg.html = message  # Use the HTML version for better formatting
    mail.send(msg)
