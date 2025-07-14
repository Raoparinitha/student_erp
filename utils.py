import smtplib
from email.mime.text import MIMEText

def send_email_alert(student_name, parent_email, percentage):
    sender = 'youremail@gmail.com'
    password = 'yourapppassword'  # Use Gmail App Password

    subject = f"Attendance Alert for {student_name}"
    body = f"""
    Dear Parent,

    This is to inform you that your child {student_name} has an attendance percentage of {percentage:.2f}%,
    which is below the required minimum of 85%.

    Kindly ensure their regular attendance.

    Regards,
    School ERP System
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = parent_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, password)
        server.sendmail(sender, parent_email, msg.as_string())
        server.quit()
        print(f"Email alert sent to {parent_email}")
    except Exception as e:
        print("Failed to send email:", e)
