from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

# Function to send an email with attachment
def send_email_with_attachment(to_address, file_path):
    from_address = "wrestler-boy1@live.com"
    from_password = "ppuqedcoerkoixaj"  # App password generated
    subject = "Completed Application - First Class Apartments"
    body = "Please find the attached completed rental application."

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    attachment = MIMEBase('application', 'octet-stream')
    with open(file_path, 'rb') as file:
        attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
    msg.attach(attachment)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(from_address, from_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

@app.route('/')
def index():
    return render_template('Application.html')

@app.route('/submit_application', methods=['POST'])
def submit_application():
    # Here you would handle the form data, for this example we assume the form is valid
    recipient_email = "OliverSlapinski@hotmail.com"
    pdf_file = "application-3.pdf"  # Ensure this file exists in the same directory as app.py
    
    # Send email with PDF attachment
    send_email_with_attachment(recipient_email, pdf_file)
    
    return "Email with the completed application sent."

if __name__ == '__main__':
    app.run(debug=True)
