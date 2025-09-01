# Uber Receipt Scraper

This project contains Python scripts designed to scrape Uber receipts from email inboxes to calculate and analyze expenses. It uses IMAP to connect to email servers, parse emails, and extract relevant data such as trip dates and costs.

## Features

- **Email Scraping**: Connects to an IMAP server (Gmail, Outlook, etc.) to fetch Uber receipt emails.
- **Data Extraction**: Parses email content to extract key information like the date and total fare of each trip.
- **Multi-Account Support**: An advanced version of the script supports fetching receipts from multiple email accounts (e.g., migrating from Outlook to Gmail).
- **Data Aggregation**: Combines extracted data for comprehensive expense analysis.

## Prerequisites

- Python 3.x
- Basic knowledge of how to enable IMAP access in your email account (Gmail, Outlook, etc.).
- For Gmail, you might need to generate an "App Password" to allow the script to log in.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jeffthedeveloper/uberscraping.git
    cd uberscraping
    ```

2.  **(Optional) Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies (if any):**
    This script only uses standard Python libraries, but for data analysis, you might want to install Pandas:
    ```bash
    pip install pandas
    ```

## Scripts Overview

### 1. `uberScraping.py` (Single Account)

This is a simple script designed to connect to a single email account, search for Uber receipts based on sender and subject, and extract the date and fare from the email body.

#### Usage

1.  Open the `uberScraping.py` file.
2.  Replace the placeholder credentials (`YOUR_EMAIL@gmail.com`, `YOUR_APP_PASSWORD`) with your actual email and password (or App Password).
3.  Run the script:
    ```bash
    python uberScraping.py
    ```

### 2. `uberScraping2.py` (Multi-Account)

This script is an advanced version that can fetch receipts from two different email accounts (e.g., Outlook and Gmail) and merge the results. It's useful if you've switched email providers and want to consolidate all your historical data.

#### Usage

1.  Open the `uberScraping2.py` file.
2.  Fill in the placeholder credentials for both Outlook and Gmail accounts.
3.  Set the `CUTOFF_DATE` variable to the date when you switched from the first email account to the second.
4.  Run the script:
    ```bash
    python uberScraping2.py
    ```

## Security Warning

**Never hardcode your credentials directly in the script if you plan to share it or upload it to a public repository.**

For better security, use one of the following methods:
- **Environment Variables**: Store your credentials as environment variables and access them in the script using `os.environ.get()`.
- **Config File**: Use a separate, untracked configuration file (e.g., `.env` or `config.ini`) to store your credentials.

## Contribution

Feel free to fork this repository, make improvements, and submit a pull request.
