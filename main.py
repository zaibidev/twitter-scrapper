from client import TwitterClient, parse_args
import logging


def main():
    args = parse_args()
    client = TwitterClient()
    tweets = client.search_tweets(
        query=args.query,
        section=args.section,
        min_retweets=args.min_retweets,
        min_likes=args.min_likes,
        limit=args.limit,
        start_date=args.start_date,
        language=args.language
    )
    if not tweets:
        logging.error("Failed to fetch tweets")


if __name__ == "__main__":
    main()
