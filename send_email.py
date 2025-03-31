from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
import os
import pickle

# Scopes required for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def authenticate_gmail():
    """Authenticate with Gmail API."""
    creds = None
    if os.path.exists('C:\\Users\\vinakhan\\.google\\token.pickle'):
        with open('C:\\Users\\vinakhan\\.google\\token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('C:\\Users\\vinakhan\\.google\\client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('C:\\Users\\vinakhan\\.google\\token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def send_email(to, subject, message_text):
    """Send an email using Gmail API."""
    service = authenticate_gmail()  # ✅ Calling authenticate_gmail here

    # Create the email message
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email
    try:
        sent_message = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print(f"Message Id: {sent_message['id']}")
        return sent_message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None

# Example usage
if __name__ == '__main__':
    recipient_email = "vinaysupermario@gmail.com"
    subject = "Test Email"
    body = "Hello, this is a test email sent using the Gmail API!"

    send_email(recipient_email, subject, body)