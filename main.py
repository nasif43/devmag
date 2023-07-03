import feedparser

feed_urls = [
    'https://dev.to/feed', 'https://hnrss.org/frontpage',
    'https://medium.com/feed/tag/openai',
    'https://medium.com/feed/tag/data-science', 'https://medium.com/feed/tag/ml',
    'https://arstechnica.com/tech-policy/feed/',
    'https://www.smashingmagazine.com/feed/',
    'https://feed.infoq.com/architecture-design/',
    'https://www.theverge.com/tech/rss/index.xml',
    'https://www.phoronix.com/rss.php', 'https://opensource.com/feed',
    'https://www.linuxjournal.com/node/feed'
]

desired_tags = [
    'machine-learning', 'artificial-intelligence', 'data-science', 'openai',
    'chatgpt'
]

for feed_url in feed_urls:
    try:
        feed = feedparser.parse(feed_url)

        # Access feed information
        feed_title = feed.feed.title
        feed_description = feed.feed.description

        print("Feed Title:", feed_title)
        print("Feed Description:", feed_description)
        print()
    except Exception as e:
        print(e)

    # Access and process individual entries in the feed
    for entry in feed.entries:
        entry_title = entry.title
        entry_link = entry.link
        entry_published = entry.published
        entry_summary = entry.summary
        try:
            entry_tags = [tag.term.lower() for tag in entry.tags]
            entry_categories = [
                category.term.lower() for category in entry.get('tags', [])
            ]
            entry_keywords = [
                keyword.lower() for keyword in entry.get('keywords', [])
            ]
            if any(
                    tag in entry_tags or tag in entry_categories or tag in entry_keywords
                    for tag in desired_tags):
                print("Title:", entry_title)
                print("Link:", entry_link)
                print("Published:", entry_published)
                print("Tags:", entry_tags)
                # print("Summary:", entry_summary)
                print()
        except Exception as e:
            print("Title:", entry_title)
            print("Link:", entry_link)
            print("Published:", entry_published)
            print("Tags:", e)
            print()

    print("---" * 10)  # Separator between different feeds
