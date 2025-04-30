# Attachments.py
import imaplib
import ssl
import email
import os
from pathlib import Path
from getpass import getpass
from datetime import datetime, timedelta

def download_pdfs(folder_path, email_user, email_pass):
    context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL("imap.gmail.com", port=993, ssl_context=context)
    mail.login(email_user, email_pass)
    mail.select('Inbox')

    date = (datetime.now() - timedelta(1)).strftime("%d-%b-%Y")
    search_criteria = f'(SENTSINCE {date} SUBJECT "job application" BODY "job application")'
    result, data = mail.search(None, search_criteria)
    pdf_count = 0
    downloaded_files = []  # List to store downloaded file details

    if result == 'OK':
        mail_ids = data[0].split()
    else:
        print("No emails found.")
        return []

    for id in mail_ids:
        result, data = mail.fetch(id, '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            file_name = part.get_filename()

            if file_name and file_name.lower().endswith('.pdf'):
                file_path = os.path.join(folder_path, file_name)

                # Avoid overwriting files by appending a counter
                if os.path.isfile(file_path):
                    base, extension = os.path.splitext(file_name)
                    counter = 1
                    while os.path.isfile(file_path):
                        file_path = os.path.join(folder_path, f"{base}_{counter}{extension}")
                        counter += 1

                with open(file_path, 'wb') as fp:
                    fp.write(part.get_payload(decode=True))

                subject = email_message['Subject'] if email_message['Subject'] else "No Subject"
                downloaded_files.append(f'Downloaded "{file_name}" from email titled "{subject}".')
                pdf_count += 1
 
    mail.logout()
    return downloaded_files, pdf_count  # Return the list of downloaded files
