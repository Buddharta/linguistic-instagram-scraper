import json
import csv
import os
import glob

def process_comments_to_csv(json_file, output_csv=None):
    """
    Convert comments JSON to CSV with columns: username, user_id, post_url, comment_text
    """
    # Auto-generate output filename if not provided
    if output_csv is None:
        base_name = os.path.basename(json_file)[:-5]
        output_csv = f"outputs/{base_name}_processed.csv"
    
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Prepare CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['username', 'comment_id', 'post_url', 'post_hashtags', 'comment_text'])
        
        # Process each post
        for post in data:
            post_url = post.get('url', '')
            post_caption = post.get('caption', '')
            if post_caption and '#' in post_caption: #Process only comments with hashtags 
                caption_words = post_caption.split()
                post_hashtags=" "
                for word in caption_words:
                    if word.startswith('#'):
                        post_hashtags+=f'{word} '
            else:
                post_hashtags="N/A"
            # Process each comment
            for comment in post.get('comments', []):
                username = comment.get('owner', '')
                comment_id = comment.get('id', '')
                comment_text = comment.get('text', '')
                
                # Write row
                writer.writerow([username, comment_id, post_url, post_hashtags, comment_text])
                
                # Also process replies if they exist
                for reply in comment.get('replies', []):
                    reply_username = reply.get('owner', '')
                    reply_id = reply.get('id', '')
                    reply_text = reply.get('text', '')
                    writer.writerow([reply_username, reply_id, post_url, reply_text])
    
    print(f"CSV saved to: {output_csv}")
    return output_csv

# Process all JSON files in current directory
json_files = glob.glob('data/*_comments.json')

if json_files:
    for json_file in json_files:
        print(f"Processing {json_file}...")
        process_comments_to_csv(json_file)
else:
    print("No *_comments.json files found in current directory")
    
    # Or specify a specific file:
    # process_comments_to_csv('vickywolff_comments.json')
