import streamlit as st
import feedparser
from bs4 import BeautifulSoup
import requests
from itertools import cycle

feed_urls = [
    'https://dev.to/feed', 'https://hnrss.org/frontpage',
    'https://medium.com/feed/tag/openai',
    'https://medium.com/feed/tag/data-science', 'https://medium.com/feed/tag/ml',
    'https://arstechnica.com/tech-policy/feed/',
    'https://www.smashingmagazine.com/feed/',
    'https://feed.infoq.com/architecture-design/',
    'https://www.theverge.com/tech/rss/index.xml',
]

# List of available tags for selection
available_tags = [
    'machine-learning', 'artificial-intelligence', 'data-science', 'openai',
    'chatgpt', 'neural-networks', 'deep-learning', 'natural-language-processing',
    'computer-vision', 'reinforcement-learning', 'robotics', 'automation',
    'ethics-in-ai', 'machine-vision', 'data-analysis', 'predictive-analytics',
    'big-data', 'data-mining', 'data-visualization', 'cloud-computing',
    'programming', 'algorithms', 'tech-news', 'innovation', 'future-tech'
]


# Dictionary to assign colors to tags
tag_colors = {
    'machine-learning': 'purple',
    'artificial-intelligence': 'blue',
    'data-science': 'green',
    'openai': 'orange',
    'chatgpt': 'red'
}

st.title("RSS Feed Reader")

# Initialize selected_tags
selected_tags = st.multiselect("Select Tags", available_tags, default=available_tags)

# Function to color code tags
def colorize_tags(tags):
    color_cycle = cycle(list(tag_colors.values()))
    colored_tags = [f'<span style="color:{next(color_cycle)}">{tag}</span>' for tag in tags]
    return ', '.join(colored_tags)

def filter_entries_with_selected_tags(entry):
    if 'tags' in entry:
        entry_tags = [tag.term.lower() for tag in entry.tags]
        return any(tag in entry_tags for tag in selected_tags)
    return False

for feed_url in feed_urls:
    try:
        feed = feedparser.parse(feed_url)
        feed_title = feed.feed.title
        feed_description = feed.feed.description

        st.header(feed_title)
        st.write(feed_description)
    except Exception as e:
        st.error(str(e))

    filtered_entries = [entry for entry in feed.entries if filter_entries_with_selected_tags(entry)]

    for entry in filtered_entries:
        entry_title = entry.title
        entry_link = entry.link
        entry_published = entry.published
        entry_tags = [tag.term.lower() for tag in entry.get('tags', [])]

        try:
            # Extract article details using BeautifulSoup
            response = requests.get(entry_link)
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tag = soup.find('meta', {'property': 'og:image'})
            img_url = img_tag['content'] if img_tag else None
        except Exception as e:
            img_url = None

        st.subheader(entry_title)
        st.write(f"Link: [{entry_link}]({entry_link})")
        st.write(f"Published: {entry_published}")
        if img_url:
            st.image(img_url, caption='Article Image', use_column_width=True)
        st.write(f"Tags: {colorize_tags(entry_tags)}", unsafe_allow_html=True)
        st.write("---")
