import smtplib, ssl
import os
from string import Template
import glob
import shutil
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv

dotenv_path = os.path.join('.env')
load_dotenv(dotenv_path)

MY_ADDRESS = os.environ.get('MY_ADDRESS')
PASSWORD = os.environ.get('PASSWORD')
#filepath_name = r'\\for_output\\output.xlsx'

src = glob.glob('C:/Dev/compare_reports_KUPOL_1C/compare_reports_KUPOL_1C/save/so_report/*.xlsx') # * means all if need specific format then *.csv
src = max(src, key=os.path.getctime)
dest = 'C:\DEV\compare_reports_KUPOL_1C\sends'
copy = shutil.copy2(src, dest)
print(copy)

def get_filename():
    list_of_files = glob.glob('C:/Dev/compare_reports_KUPOL_1C/compare_reports_KUPOL_1C/save/so_report/*.xlsx') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    #filename = os.path.basename(latest_file)
    #print(filename)
    return latest_file

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    names, emails = get_contacts(r'C:\DEV\compare_reports_KUPOL_1C\compare_reports_KUPOL_1C\mycontacts.txt') # read contacts
    message_template = read_template(r'C:\DEV\compare_reports_KUPOL_1C\compare_reports_KUPOL_1C\message.txt')
    filename_template = get_filename()
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(filename_template, "rb").read())
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename_template)
    encoders.encode_base64(part)
    context = ssl._create_unverified_context()

    # set up the SMTP server
    s = smtplib.SMTP(host='dag.nord.local', port=465)
    s.starttls(context=context)
    s.login(MY_ADDRESS, PASSWORD)
    

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Сверка списаний между КУПОЛ и 1С"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        msg.attach(part)
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()    
    time.sleep(5)