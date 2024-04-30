from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/submit_application', methods=['POST'])
def submit_application():
    # Extracting form data
    fullname = request.form['fullname']
    email = request.form['email']
    address = request.form['address']
    phone = request.form['phone']
    tenantRef = request.form['tenantRef']
    rentPaid = request.form['rentPaid']
    occupancyType = request.form['occupancyType']
    criminalRecord = request.form['criminalRecord']
    employment = request.form['employment']

    # Create the email content
    email_subject = "New Application from " + fullname
    email_body = f"""
    New application received:
    
    Full Name: {fullname}
    Email: {email}
    Address: {address}
    Phone: {phone}
    Tenant Reference: {tenantRef}
    Rent Paid: {rentPaid}
    Occupancy Type: {occupancyType}
    Criminal Record: {criminalRecord}
    Employment Status: {employment}
    """

    # Email setup
    sender_email = "your-email@example.com"  # Replace with your email
    receiver_email = "landlord-email@example.com"  # Replace with landlord's email
    password = "your-password"  # Replace with your email password

    # Create a secure SSL context
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = email_subject

    # Add body to email
    message.attach(MIMEText(email_body, "plain"))

    # Send the email
    with smtplib.SMTP_SSL('smtp.example.com', 465) as server:  # Replace with your SMTP server
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return 'Application Submitted Successfully'

if __name__ == '__main__':
    app.run(debug=True)
