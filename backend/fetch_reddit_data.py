import praw
import sqlite3

# Configure PRAW with your Reddit API credentials
reddit = praw.Reddit(
    client_id="24IJ-eNB7h4J643O6ljulw",       # Replace with your client_id
    client_secret="AtzVpukDay5Z_Iyhvlkf-DPJ3AuwUQ",  # Replace with your client_secret
    user_agent="SubTrendsApp/0.1 by JeanDaDon"  # Replace with your Reddit username
)

conn = sqlite3.connect('subtrends.db')
cursor = conn.cursor()

def fetch_subreddit_data(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)

    posts = []
    for post in subreddit.hot(limit=limit):
        posts.append((
        post.id,
        post.title,
        post.score,
        post.num_comments,
        post.created_utc
))

    # Insert posts into the database
    cursor.executemany('''
    INSERT OR IGNORE INTO posts (id, title, score, num_comments, created_at)
    VALUES (?, ?, ?, ?, datetime(?, 'unixepoch'))
    ''', posts)

    conn.commit()
    print(f"Inserted {len(posts)} posts from r/{subreddit_name} into the database!")

# Fetch data from your desired subreddit
fetch_subreddit_data('technology', limit=10)

# Close the database connection
conn.close()