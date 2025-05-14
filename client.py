import os
import logging
import argparse
from dotenv import load_dotenv
import requests
from utils import SpreadsheetManager

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://twitter154.p.rapidapi.com/search/search"

class TwitterClient:
    def __init__(self):
        self.headers = {
            "x-rapidapi-host": "twitter154.p.rapidapi.com",
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY")
        }
        self.spreadsheet_manager = SpreadsheetManager()
        self._init_spreadsheets()

    def _init_spreadsheets(self):
        # Get initial records to ensure sheets exist
        self.account_records = self.spreadsheet_manager.get_all_accounts()
        self.tweet_records = self.spreadsheet_manager.get_all_tweets()

    def search_tweets(self, query, section="top", min_retweets=0, min_likes=0, 
                     limit=10, start_date=None, language="en"):
        params = {
            "query": query,
            "section": section,
            "min_retweets": min_retweets,
            "min_likes": min_likes,
            "limit": limit,
            "language": language
        }
        if start_date:
            params["start_date"] = start_date

        try:
            response = requests.get(BASE_URL, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            for tweet in data.get("results", []):
                self._process_tweet(tweet)
            
            logging.info(f"Successfully processed {len(data.get('results', []))} tweets")
            return data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during API request: {str(e)}")
            return None

    def _process_tweet(self, tweet):
        user = tweet.get("user", {})
        handle = user.get("username")
        
        # Process user data
        if not any(record["Twitter Handle"] == handle for record in self.account_records):
            self._save_user_data(user)
        
        # Process tweet data
        tweet_id = tweet.get("tweet_id")
        if not any(record["Tweet ID"] == tweet_id for record in self.tweet_records):
            self._save_tweet_data(tweet, handle)

    def _save_user_data(self, user):
        handle = user.get("username")
        name = user.get("name")
        followers = user.get("follower_count", 0)
        location = user.get("location", "Unknown")
        description = user.get("description", "No description")
        self.spreadsheet_manager.save_account(handle, name, followers, location, description)
        self.account_records = self.spreadsheet_manager.get_all_accounts()
        logging.info(f"Added new account: {handle}")

    def _save_tweet_data(self, tweet, handle):
        tweet_id = tweet.get("tweet_id")
        text = tweet.get("text")
        retweets = tweet.get("retweet_count", 0)
        likes = tweet.get("favorite_count", 0)
        date = tweet.get("creation_date")
        self.spreadsheet_manager.save_tweet(tweet_id, handle, text, retweets, likes, date)
        self.tweet_records = self.spreadsheet_manager.get_all_tweets()
        logging.info(f"Added new tweet: {tweet_id}")

def parse_args():
    parser = argparse.ArgumentParser(description="Twitter Search Tool")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--section", default="top", choices=["top", "latest"], help="Section to search")
    parser.add_argument("--min-retweets", type=int, default=0, help="Minimum number of retweets")
    parser.add_argument("--min-likes", type=int, default=0, help="Minimum number of likes")
    parser.add_argument("--limit", type=int, default=10, help="Number of results to return")
    parser.add_argument("--start-date", help="Start date in YYYY-MM-DD format")
    parser.add_argument("--language", default="en", help="Language code")
    return parser.parse_args()