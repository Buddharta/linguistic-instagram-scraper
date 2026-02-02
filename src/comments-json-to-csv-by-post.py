import json
import csv
import os
import glob

def process_comments_to_csv_by_post(json_file, output_csv=None):
    """
    Convert comments JSON to CSV with columns:post_url, username, comment_id, comment_text
    """
    # Auto-generate output filename if not provided
    if output_csv is None:
        user_name = os.path.basename(json_file)[:-14]
        base_name = os.path.basename(json_file)[:-5]
        out_dir=f"outputs/{user_name}/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            print(f"Directory '{out_dir}' created...")
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f) 
        # Process each post
        for post in data:
            url = post.get('url', '')
            post_id = post.get('shortcode', '')
            post_caption = post.get('caption', '')
            if post_caption and '#' in post_caption: #Process only comments with hashtags 
                # Process each comment
                output_csv = f"outputs/{user_name}/{base_name}_{post_id}.csv"
                caption_words = post_caption.split()
                header=[url, 'hashtags:']
                for word in caption_words:
                    if word.startswith('#'):
                        header.append(word)
                # Prepare CSV
                with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile) 
                    # Write header
                    writer.writerow(header)
                    writer.writerow(['username', 'comment_id', 'text']) 
                    for comment in post.get('comments', []):
                        username = comment.get('owner', '')
                        comment_id = str(comment.get('id', ''))
                        comment_text = comment.get('text', '')
                        # Write row
                        writer.writerow([username, comment_id, comment_text])
                        
                        # Also process replies if they exist
                        for reply in comment.get('replies', []):
                            reply_username = reply.get('owner', '')
                            reply_id = reply.get('id', '')
                            reply_text = reply.get('text', '')
                            writer.writerow([reply_username, reply_id, reply_text])
        
                print(f"CSV saved to: {output_csv}")
            else:
                print(f"Post: {url} contains no caption skipping...")

# Process all JSON files in current directory
json_files = glob.glob('data/*_comments.json')

if json_files:
    for json_file in json_files:
        print(f"Processing json file: {json_file}...")
        process_comments_to_csv_by_post(json_file)
else:
    print("No *_comments.json files found in current directory")
    
    # Or specify a specific file:
    # process_comments_to_csv('vickywolff_comments.json')
