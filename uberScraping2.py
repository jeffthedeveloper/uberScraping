import imaplib
import email
import re
import datetime
import os

# --- Configuration ---
# It is strongly recommended to use environment variables for your credentials.
# --- Outlook Account ---
EMAIL_ACCOUNT_OUTLOOK = os.environ.get('OUTLOOK_USER', "your_email@outlook.com")
PASSWORD_OUTLOOK = os.environ.get('OUTLOOK_PASSWORD', "your_outlook_password")
IMAP_SERVER_OUTLOOK = "outlook.office365.com"

# --- Gmail Account ---
EMAIL_ACCOUNT_GMAIL = os.environ.get('GMAIL_USER', "your_email@gmail.com")
PASSWORD_GMAIL = os.environ.get('GMAIL_APP_PASSWORD', "your_gmail_app_password")
IMAP_SERVER_GMAIL = "imap.gmail.com"

# --- Cutoff Date ---
# Date to switch from fetching from Outlook to Gmail
CUTOFF_DATE = datetime.datetime(2024, 3, 15)

def get_receipts_from_account(server, account, password, date_filter=None):
    """
    Generic function to fetch Uber receipts from a given email account.
    'date_filter' should be a string in IMAP search format, e.g., 'SINCE "15-Mar-2024"'
    """
    receipts = []
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(account, password)
        mail.select("inbox")

        # Build search query
        search_query = '(FROM "uber" SUBJECT "Your Uber receipt")'
        if date_filter:
            search_query = f'({search_query} {date_filter})'
        
        status, messages = mail.search(None, search_query)
        if status != 'OK':
            return []

        for num in messages[0].split():
            _, data = mail.fetch(num, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    if msg.is_multipart():
                        for part in msg.walk():
                            try:
                                body = part.get_payload(decode=True).decode()
                                fare_match = re.search(r'R\$\s*([\d,]+)', body)
                                date_match = re.search(r'\d{1,2} de \w+ de \d{4}', body)
                                if fare_match and date_match:
                                    fare_str = fare_match.group(1).replace(',', '.')
                                    receipts.append((date_match.group(0), float(fare_str)))
                                    break
                            except:
                                continue
        mail.close()
        mail.logout()
    except Exception as e:
        print(f"Failed to connect to {account}: {e}")
    return receipts

if __name__ == "__main__":
    # Fetch receipts from Outlook BEFORE the cutoff date
    outlook_date_filter = f'BEFORE "{CUTOFF_DATE.strftime("%d-%b-%Y")}"'
    print(f"Fetching receipts from Outlook {outlook_date_filter}...")
    receipts_outlook = get_receipts_from_account(IMAP_SERVER_OUTLOOK, EMAIL_ACCOUNT_OUTLOOK, PASSWORD_OUTLOOK, outlook_date_filter)
    print(f"Found {len(receipts_outlook)} receipts in Outlook.")

    # Fetch receipts from Gmail ON or AFTER the cutoff date
    gmail_date_filter = f'SINCE "{CUTOFF_DATE.strftime("%d-%b-%Y")}"'
    print(f"Fetching receipts from Gmail {gmail_date_filter}...")
    receipts_gmail = get_receipts_from_account(IMAP_SERVER_GMAIL, EMAIL_ACCOUNT_GMAIL, PASSWORD_GMAIL, gmail_date_filter)
    print(f"Found {len(receipts_gmail)} receipts in Gmail.")

    # Combine all receipts
    all_receipts = receipts_outlook + receipts_gmail

    if all_receipts:
        print(f"\nTotal receipts found: {len(all_receipts)}")
        total_spent = sum(fare for _, fare in all_receipts)
        print(f"Total combined expenses: R$ {total_spent:.2f}")
    else:
        print("\nNo receipts found in either account.")
