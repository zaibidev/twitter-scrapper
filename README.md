# Twitter Scraper

A Python-based Twitter scraping tool that searches for tweets and saves both tweet data and user information to Google Sheets.

## Features

- Search tweets with customizable parameters
- Store tweet data in Google Sheets automatically
- Track user information including followers, location, and description
- Configurable search criteria (retweets, likes, language, etc.)
- Automatic duplicate prevention for both tweets and user data

## Prerequisites

- Python 3.10 or higher
- Google Service Account credentials
- RapidAPI key for Twitter API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/twitter-scrapper.git
cd twitter-scrapper
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in a `.env` file:
```
RAPIDAPI_KEY=your_rapidapi_key
GOOGLE_SERVICE_ACCOUNT_JSON=path_to_your_service_account.json
SPREADSHEET_NAME=your_google_spreadsheet_name
```

## Usage

Run the script using command line arguments:

```bash
python main.py --query "your search term" [options]
```

Available options:
- `--query`: Search query (required)
- `--section`: Section to search ("top" or "latest", default: "top")
- `--min-retweets`: Minimum number of retweets (default: 0)
- `--min-likes`: Minimum number of likes (default: 0)
- `--limit`: Number of results to return (default: 10)
- `--start-date`: Start date in YYYY-MM-DD format
- `--language`: Language code (default: "en")

Example:
```bash
python main.py --query "python programming" --min-likes 100 --limit 20
```

## Data Storage

The script stores data in two Google Sheets worksheets:

1. **Accounts**:
   - Twitter Handle
   - Name
   - Followers
   - Location
   - Description

2. **Tweets**:
   - Tweet ID
   - Twitter Handle
   - Text
   - Retweets
   - Likes
   - Date

## Error Handling

- The script includes comprehensive error handling and logging
- Failed API requests are logged with detailed error messages
- Duplicate entries are automatically detected and skipped