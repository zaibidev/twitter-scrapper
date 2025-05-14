import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

class SpreadsheetManager:
    def __init__(self):
        self.scope = ["https://spreadsheets.google.com/feeds", 
                     "https://www.googleapis.com/auth/spreadsheets",
                     "https://www.googleapis.com/auth/drive"]
        self.creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        self.spreadsheet_name = os.getenv("SPREADSHEET_NAME")
        self._initialize_connection()

    def _initialize_connection(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, self.scope)
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open(self.spreadsheet_name)
        self._ensure_worksheets_exist()

    def _ensure_worksheets_exist(self):
        try:
            self.accounts_sheet = self.spreadsheet.worksheet("Accounts")
        except gspread.exceptions.WorksheetNotFound:
            self.accounts_sheet = self.spreadsheet.add_worksheet(title="Accounts", rows="100", cols="5")
            self.accounts_sheet.append_row(["Twitter Handle", "Name", "Followers", "Location", "Description"])

        try:
            self.tweets_sheet = self.spreadsheet.worksheet("Tweets")
        except gspread.exceptions.WorksheetNotFound:
            self.tweets_sheet = self.spreadsheet.add_worksheet(title="Tweets", rows="1000", cols="6")
            self.tweets_sheet.append_row(["Tweet ID", "Twitter Handle", "Text", "Retweets", "Likes", "Date"])

    def save_account(self, handle, name, followers, location, description):
        self.accounts_sheet.append_row([handle, name, followers, location, description])

    def save_tweet(self, tweet_id, handle, text, retweets, likes, date):
        self.tweets_sheet.append_row([tweet_id, handle, text, retweets, likes, date])

    def get_all_accounts(self):
        return self.accounts_sheet.get_all_records()

    def get_all_tweets(self):
        return self.tweets_sheet.get_all_records()