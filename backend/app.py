from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to fetch all posts
def fetch_posts():
    conn = sqlite3.connect('subtrends.db')  # Connect to the database
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, title, score, num_comments, created_at FROM posts')  # Query all posts
    rows = cursor.fetchall()  # Fetch all rows
    
    conn.close()
    
    # Convert rows into a list of dictionaries
    posts = []
    for row in rows:
        posts.append({
            'id': row[0],
            'title': row[1],
            'score': row[2],
            'num_comments': row[3],
            'created_at': row[4]
        })
    
    return posts

# Function to filter posts by score
def fetch_filtered_posts(min_score):
    conn = sqlite3.connect('subtrends.db')  # Connect to the database
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, title, score, num_comments, created_at
    FROM posts
    WHERE score >= ?
    ''', (min_score,))
    rows = cursor.fetchall()  # Fetch all matching rows
    
    conn.close()
    
    # Convert rows into a list of dictionaries
    posts = []
    for row in rows:
        posts.append({
            'id': row[0],
            'title': row[1],
            'score': row[2],
            'num_comments': row[3],
            'created_at': row[4]
        })
    
    return posts

# Route: Home (Sanity check)
@app.route('/')
def home():
    return "Welcome to SubTrends! Use the endpoints to access Reddit post data."

# Route: Get all posts
@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = fetch_posts()  # Fetch all posts from the database
    return jsonify(posts)

# Route: Get filtered posts
@app.route('/posts/filter', methods=['GET'])
def get_filtered_posts():
    min_score = int(request.args.get('min_score', 0))  # Default to 0 if not provided
    posts = fetch_filtered_posts(min_score)  # Fetch filtered posts
    return jsonify(posts)

# Route: Get a single post by ID
@app.route('/posts/<post_id>', methods=['GET'])
def get_post_by_id(post_id):
    conn = sqlite3.connect('subtrends.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, title, score, num_comments, created_at
    FROM posts
    WHERE id = ?
    ''', (post_id,))
    row = cursor.fetchone()  # Fetch one row
    
    conn.close()
    
    if row is None:
        return jsonify({"error": "Post not found"}), 404
    
    post = {
        'id': row[0],
        'title': row[1],
        'score': row[2],
        'num_comments': row[3],
        'created_at': row[4]
    }
    
    return jsonify(post)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run the server on port 5001