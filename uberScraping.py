import imaplib
import email
import re
import os
from email.header import decode_header

# --- Configuration ---
# For security, it is recommended to use environment variables instead of hardcoding credentials.
# Example: EMAIL_ACCOUNT = os.environ.get('GMAIL_USER')
EMAIL_ACCOUNT = "YOUR_EMAIL@gmail.com"
PASSWORD = "YOUR_APP_PASSWORD"  # For Gmail, use an "App Password"
IMAP_SERVER = "imap.gmail.com"

def get_uber_receipts():
    """
    Connects to an email account, fetches Uber receipts, and extracts trip data.
    """
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        mail.select("inbox")

        # Search for emails from Uber with a specific subject
        # Note: You may need to adjust the search criteria based on your email language and format
        status, messages = mail.search(None, '(FROM "uber" SUBJECT "Your Uber receipt")')

        if status != 'OK':
            print("No messages found!")
            return []

        receipts = []
        message_ids = messages[0].split()

        for num in message_ids:
            status, data = mail.fetch(num, '(RFC822)')
            if status == 'OK':
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Decode the email body
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    continue
                                
                                if content_type == "text/plain" or content_type == "text/html":
                                    # Use regex to find date and fare. Adjust regex as needed.
                                    # Example for "25 de agosto de 2024"
                                    date_match = re.search(r'\d{1,2} de \w+ de \d{4}', body)
                                    # Example for "R$ 25,50"
                                    fare_match = re.search(r'R\$\s*([\d,]+)', body)

                                    if date_match and fare_match:
                                        date_str = date_match.group(0)
                                        # Standardize fare to use dot as decimal separator
                                        fare_str = fare_match.group(1).replace(',', '.')
                                        receipts.append((date_str, float(fare_str)))
                                        # Break after finding the first match in the parts
                                        break
                        else:
                             # Handle non-multipart messages (less common for HTML emails)
                            pass


        mail.close()
        mail.logout()
        return receipts

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    receipts_data = get_uber_receipts()

    if receipts_data:
        print(f"Found {len(receipts_data)} receipts.")
        # Example of processing: calculate total expenses
        total_spent = sum(fare for date, fare in receipts_data)
        print(f"Total amount spent on Uber: R$ {total_spent:.2f}")
        # print("\nReceipts Details:")
        # for date, fare in receipts_data:
        #     print(f"Date: {date}, Fare: R$ {fare:.2f}")
    else:
        print("Could not retrieve any receipt data.")
