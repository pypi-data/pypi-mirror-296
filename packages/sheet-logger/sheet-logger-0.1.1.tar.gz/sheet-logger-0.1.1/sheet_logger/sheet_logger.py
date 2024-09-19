# sheet_logger.py
from pathlib import Path
from google.oauth2.credentials import Credentials
import sys
from datetime import datetime
import time

class SheetLogger:
    """
    A logger that appends log messages to specific Google Sheets tabs with batching, timestamping, and API rate limit checks.
    
    Features:
        - Timestamps: Automatically prepends log messages with a timestamp ("YYYY-MM-DD HH:MM:SS").
        - Batching: Accumulates log entries and writes them in batches to reduce API calls (batch size is configurable).
        - API Rate Limit: Monitors and enforces Google's 60 API requests per minute limit, pausing if necessary.
    
    Attributes:
        spreadsheet_id (str): Google Spreadsheet ID.
        service (obj): Google Sheets API service object.
        logs (dict): Stores log messages by tab.
        batch_size (int): Number of log entries to accumulate before flushing to the sheet.
        batch_data (list): Stores batched data before sending to the sheet.
        api_write_counter (int): Tracks API write calls.
        api_write_reset_time (datetime): Tracks time for resetting API rate limit counter.
    
    Methods:
        write_to_sheet(tab_name, message): Adds a log entry with a timestamp to the specified tab and flushes if batch size is reached.
        flush(tab_name): Writes accumulated batch data to the specified tab.
        check_api_limit(): Ensures API write calls do not exceed 60 requests per minute.

    Example Usage:
    Log call: sheet_logger.write_to_sheet(tab_name, message)
    Log output format: "YYYY-MM-DD HH:MM:SS - message"
    """

    def __init__(self, spreadsheet_id, scopes, batch_size=5, token_full_path=None, subfolder=None, token_file_name="token.json"):
        """
        Initializes the SheetLogger by obtaining Google Sheets API credentials, setting up logs, and batch settings.
        Args:
            spreadsheet_id (str): The ID of the Google Spreadsheet.
            scopes (list): The API access scopes for Google Sheets.
            batch_size (int): Number of log entries to batch before writing to the sheet (default is 5).
            subfolder (str): Optional subfolder where the token file is located.
            token_file_name (str): The name of the token file (default is "token.json").
        """
        self.spreadsheet_id = spreadsheet_id
        self.token_full_path = token_full_path
        self.token_file_name = token_file_name
        self.subfolder = subfolder
        self.service = self.get_service(scopes)
        self.logs = {}  ## Dynamic log storage for tabs
        self.batch_size = batch_size
        self.batch_data = []
        self.api_write_counter = 0
        self.api_write_reset_time = datetime.now()

    def get_service(self, scopes):
        """
        Sets up the Google Sheets API service using the provided scopes and returns
        Google Sheets service object or None if credentials couldn't be obtained.
        """
        creds = self.get_token_creds(scopes)
        if creds:
            from googleapiclient.discovery import build
            return build('sheets', 'v4', credentials=creds)
        else:
            print("Error: Could not obtain credentials.")
            return None

    def get_token_creds(self, scopes):
        """
        Obtains or refreshes token credentials for the specified API scopes and
        returns the credentials object or None if credentials couldn't be loaded.
        """
        creds = None
        try:
            ## Check if the token file path is provided; otherwise, use the default location
            if self.token_full_path:
                token_file = Path(self.token_full_path)

            else:
                ## Determine current working directory and handle Jupyter or script execution
                if "ipykernel" in sys.modules:  ## Running in a Jupyter notebook
                    current_dir = Path().resolve()
                    parent_dir = current_dir.parent
                else:  ## Running in a .py script
                    current_dir = Path(__file__).resolve()
                    parent_dir = current_dir.parent.parent

                ## If a subfolder is provided, use it; otherwise, just use the parent directory
                token_file = parent_dir / self.subfolder / self.token_file_name if self.subfolder else parent_dir / self.token_file_name

            ## Check if the token file exists
            if not token_file.exists():
                raise FileNotFoundError(f"Error: token.json not found at {token_file}. "
                                        "Make sure the file is located in the correct folder.")
            
            ## Load the token credentials from the 'token.json' file
            creds = Credentials.from_authorized_user_file(token_file, scopes)
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return creds

    def check_api_limit(self):
        """
        Checks if the API call limit has been reached and waits for reset if necessary.
        Google Sheets has a rate limit of 60 requests per user per minute.
        """
        elapsed_time = (datetime.now() - self.api_write_reset_time).total_seconds()
        if elapsed_time < 60:
            if self.api_write_counter >= 59:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - API limit reached. Pausing for 60 seconds.")
                time.sleep(60)
                self.api_write_counter = 0
                self.api_write_reset_time = datetime.now()
        else:
            self.api_write_counter = 0
            self.api_write_reset_time = datetime.now()

    def write(self, message, tab_name):
        """
        Adds a log message to the specified sheet tab and batches it.
        NOTE: Appends each line of the message to the logs for the specified tab,
        with a timestamp in the format "YYYY-MM-DD HH:MM:SS -".
        """
        if tab_name not in self.logs:
            self.logs[tab_name] = []  ## Dynamically add tab names if they don't already exist

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} - {message}"

        lines = formatted_message.split('\n')
        for line in lines:
            if line:  ## Only append non-empty lines
                self.logs[tab_name].append([line])
                self.batch_data.append([line])

        ## Flush the data if batch size limit is reached
        if len(self.batch_data) >= self.batch_size:
            self.flush(tab_name)

    def flush(self, tab_name):
        """
        Flushes all logs stored for the specified tab to the Google Sheet in batches.
        """
        if self.batch_data:
            self.check_api_limit()  ## Ensure API limit is respected before writing
            try:
                ## Batch writing to Google Sheet
                self.service.spreadsheets().values().append(
                    spreadsheetId=self.spreadsheet_id,
                    range=f'{tab_name}!A:B',
                    valueInputOption='RAW',
                    insertDataOption='INSERT_ROWS',
                    body={'values': self.batch_data}
                ).execute()

                self.batch_data = []  ## Clear batch after flushing
                self.api_write_counter += 1  ## Increment API write call counter
            except Exception as e:
                print(f"Failed to append logs: {e}", file=sys.__stdout__)

    def write_to_sheet(self, tab_name, message):
        """
        Writes a log message to a specified tab and flushes if batch size is reached.
        NOTE:
            - Dynamically adds new tab names to the logs dictionary if they don't already exist.
            - Flushes logs to the Google Sheet in batches when necessary.
        """
        self.write(message, tab_name)