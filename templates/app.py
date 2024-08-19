from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from fpdf import FPDF
import base64

app = Flask(__name__)

# Route to serve images from the templates directory
@app.route('/templates/<path:filename>')
def custom_static(filename):
    return send_from_directory('templates', filename)

def create_pdf(form_data, signatures):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Application to Rent - First Class Apartments', 0, 1, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(5)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)
            self.ln()

        def add_image(self, field, img_data):
            if img_data:
                img_data = img_data.split(',')[1]
                img_file = f'{field}.png'
                with open(img_file, 'wb') as f:
                    f.write(base64.b64decode(img_data))
                self.image(img_file, x=10, y=self.get_y(), w=100)
                os.remove(img_file)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    for key, value in form_data.items():
        pdf.cell(0, 10, f'{key.replace("_", " ").capitalize()}: {value}', 0, 1)
    
    for key, value in signatures.items():
        pdf.add_image(key, value)

    applicant_name = form_data.get('applicant_name', 'Unknown').replace(' ', '_')
    address_of_rental = form_data.get('address_of_rental', 'Unknown').replace(' ', '_')
    pdf_filename = f'{applicant_name}_{address_of_rental}_Application.pdf'
    pdf.output(pdf_filename)

    print(f"PDF created: {pdf_filename}")  # Debugging line

    return pdf_filename

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
        print(f"Attempting to send email to {to_address}")  # Debugging line
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(from_address, from_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_address}!")  # Debugging line
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

@app.route('/')
def index():
    form_data = {
        'applicant_name': '',
        'address_of_rental': '',
        'contact_number': '',
        'email': '',  # Added email field
        'workers_name': '',
        'workers_contact_number': '',
        'workers_ext': '',
        'date': '',
        'address_of_premises': '',
        'occupancy_date': '',
        'legal_name': '',
        'preferred_name': '',
        'date_of_birth': '',
        'social_insurance_number': '',
        'drivers_license_number': '',
        'province_issued': '',
        'make_model_auto': '',
        'year': '',
        'plate_number': '',
        'present_residence': '',
        'how_long_present': '',
        'landlord_phone_present': '',
        'previous_address': '',
        'how_long_previous': '',
        'landlord_phone_previous': '',
        'rent_tribunal': '',
        'reason': '',
        'outcome': '',
        'credit_check': '',
        'monthly_income': '',
        'sources': '',
        'garbage': '',
        'no_cats': '',
        'snow': '',
        'drapes': '',
        'cable': '',
        'single_person': '',
        'no_noise': '',
        'no_loud_music': '',
        'rent_paid': '',
        'smoke_detectors': '',
        'emergency_contact_name': '',
        'emergency_contact_relationship': '',
        'emergency_contact_city': '',
        'emergency_contact_province': '',
        'emergency_contact_postal': '',
        'emergency_contact_day_phone': '',
        'emergency_contact_evening_phone': '',
        'emergency_contact_cell': '',
        'alt_emergency_contact_name': '',
        'alt_emergency_contact_relationship': '',
        'alt_emergency_contact_city': '',
        'alt_emergency_contact_province': '',
        'alt_emergency_contact_postal': '',
        'alt_emergency_contact_day_phone': '',
        'alt_emergency_contact_evening_phone': '',
        'alt_emergency_contact_cell': '',
        'applicant_employed_by': '',
        'applicant_occupation': '',
        'applicant_office_phone': '',
        'employed_by': '',
        'employed_occupation': '',
        'employed_office_phone': '',
        'reference1': '',
        'reference1_phone': '',
        'reference2': '',
        'reference2_phone': '',
        'signature1': '',
        'signature1_date': '',
        'signature2': '',
        'signature2_date': '',
        'witness': '',
        'witness_date': '',
    }
    return render_template('Application.html', form_data=form_data)

@app.route('/submit_application', methods=['POST'])
def submit_application():
    form_data = request.form.to_dict()
    signatures = {
        'signature': form_data.pop('signature', ''),
        'signature1': form_data.pop('signature1', ''),
        'signature2': form_data.pop('signature2', '')
    }
    pdf_file = create_pdf(form_data, signatures)
    
    recipient_email = "OliverSlapinski@hotmail.com"
    applicant_email = form_data.get('email')
    send_email_with_attachment(recipient_email, pdf_file)
    
    # Send confirmation email to the applicant
    send_email_with_attachment(applicant_email, pdf_file)
    
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('application_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
