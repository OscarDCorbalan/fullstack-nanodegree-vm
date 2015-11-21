#
# Database access functions for the web forum.
#

import bleach
import time
import psycopg2

## Database connection
DB = psycopg2.connect("dbname=forum")

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    cur = DB.cursor()
    cur.execute("SELECT content, time FROM posts ORDER BY time DESC;")
    rows = cur.fetchall()
    return [{
            'content': str(bleach.clean(row[0])),
            'time': str(row[1])
            } for row in rows]

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    query = "INSERT INTO posts (content) VALUES (%s);"
    cur = DB.cursor()
    cur.execute(query, [bleach.clean(content)])
    DB.commit()
