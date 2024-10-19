import smtplib
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendOTP(type, name, email, otp):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("innovatexservices@gmail.com", settings.EMAIL_PASSWORD)
    msg = MIMEMultipart("alternative")
    msg["subject"] = f"Verification OTP {otp}"
    msg["From"] = "innovatexservices@gmail.com"
    msg["To"] = email

    if type == "verify":
        message = "Thank you for using Quick Aid! Your one-time password (OTP) to complete the verification process is:"
    else:
        message = "Problem signing in to Quick Aid! Your one-time password (OTP) to reset your password is:"

    html_content = f"""
        <html>
    <head>
      <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }}
        .email-container {{
            max-width: 600px;
            background-color: #ffffff;
            padding: 20px;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
        }}
        .header h1 {{
            color: #3498db;
            font-size: 28px;
        }}
        .otp-message {{
            font-size: 18px;
            color: #333;
        }}
        .otp-code {{
            font-size: 36px;
            font-weight: bold;
            color: #2ecc71;
            text-align: center;
            margin: 20px 0;
            background-color: #f0f9f1;
            padding: 10px;
            border-radius: 5px;
            letter-spacing: 5px;
        }}
        .footer {{
            font-size: 14px;
            color: #888;
            text-align: center;
            margin-top: 20px;
        }}
        .footer .team {{
            font-weight: bold;
            color: #555;
        }}
      </style>
    </head>
    <body>
      <div class="email-container">
        <div class="header">
          <h1>Quick Aid</h1>
          <p>Secure & Reliable Assistance at Your Fingertips</p>
        </div>
        <p class="otp-message">Hello, {name.split()[0]}</p>
        <p class="otp-message">{message}</p>
        <p class="otp-code">{otp}</p>
        <p class="otp-message">Please enter this OTP to complete your process. It will expire in 10 minutes.</p>
        <p class="footer">If you didn't request this code, please ignore this message.</p>
        <p class="footer">Best regards,<br>The <span class="team">InnovateX</span> Team</p>
      </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    s.send_message(msg)
    s.quit()