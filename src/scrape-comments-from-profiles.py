import instaloader
import json
import time

creators=["elsocotroco","lasmacucasoficial","tilasesto","chuchopitza","lilocyv","eljuanamaro","elcronistayuc"]

# Create instance
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=True,
    save_metadata=False,
    compress_json=False,
    max_connection_attempts=3
)
# Login (recommended to avoid rate limits)
L.load_session_from_file('buddharta2')
#L.login('buddharta2', 'scrape_instagram2')  # or use L.load_session_from_file('my_user')

def retrieve_comments(target_username):
    """Retrieve all comments from a user's posts"""
    print(f"Processing {target_username}...")
    
    try:
        profile = instaloader.Profile.from_username(L.context, target_username)
    except Exception as e:
        print(f"Error loading profile {username}: {e}")
        return

# Container for all data
    all_posts_data = []

# Iterate through all posts
    for post in profile.get_posts():
        print(f"Processing post: {post.shortcode}")
        
        post_data = {
            'shortcode': post.shortcode,
            'url': f'https://www.instagram.com/p/{post.shortcode}/',
            'date': post.date_utc.isoformat(),
            'likes': post.likes,
            'caption': post.caption,
            'comments_count': post.comments,
            'comments': []
        }
        
        # Get all comments
        try:
            for comment in post.get_comments():
                comment_data = {
                    'id': comment.id,
                    'owner': comment.owner.username,
                    'text': comment.text,
                    'created_at': comment.created_at_utc.isoformat(),
                    'likes': comment.likes_count if hasattr(comment, 'likes_count') else 0,
                    'replies': []
                }
                
                # Get comment replies if they exist
                if hasattr(comment, 'answers') and comment.answers:
                    for reply in comment.answers:
                        reply_data = {
                            'id': reply.id,
                            'owner': reply.owner.username,
                            'text': reply.text,
                            'created_at': reply.created_at_utc.isoformat(),
                            'likes': reply.likes_count if hasattr(reply, 'likes_count') else 0
                        }
                        comment_data['replies'].append(reply_data)
                
                post_data['comments'].append(comment_data)
        
        except Exception as e:
            print(f"Error getting comments for {post.shortcode}: {e}")
        
        all_posts_data.append(post_data)

# Save to uncompressed JSON
    output_file = f'/home/hayt/source/Scraper/Leonor/data/{target_username}_comments.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_posts_data, f, ensure_ascii=False, indent=2)

    print(f"Data saved to {output_file}")

for user in creators:
    retrieve_comments(user)    
    time.sleep(10)  # Avoy hitting limit   
