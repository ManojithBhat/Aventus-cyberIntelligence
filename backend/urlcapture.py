import requests
from bs4 import BeautifulSoup

def extract_username_from_title(insta_url):
    # Send a GET request to the Instagram URL
    response = requests.get(insta_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the title tag
        title_tag = soup.find('title')
        
        # Extract and return the username from the title tag
        if title_tag:
            title_text = title_tag.text
            # Extract the part within parentheses and strip '@'
            start = title_text.find('(@') + 2  # Find the start of '(@' and move 2 characters forward
            end = title_text.find(')', start)  # Find the closing ')'
            if start != -1 and end != -1:
                username = title_text[start:end]
                return username
    return None
import requests
import re

def extract_instagram_stats(insta_url):
    # Send a GET request to the Instagram URL
    response = requests.get(insta_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML content as text
        html_content = response.text
        
        # Use a regex pattern to find the meta tag with the desired format
        pattern = re.compile(r'<meta content="([^"]+)" name="description" />')
        
        # Search for the pattern in the HTML content
        match = pattern.search(html_content)
        
        if match:
            # Extract the content from the matched pattern
            content = match.group(1)
            
            # Extract followers, following, and posts using another regex
            stats_match = re.search(r'([\dKM,]+) Followers, ([\dKM,]+) Following, ([\d,]+) Posts', content)
            if stats_match:
                followers = stats_match.group(1)
                following = stats_match.group(2)
                posts = stats_match.group(3)
                return followers, following, posts
    return None
"""
# Example usage
insta_url = 'https://www.instagram.com/santhoshprathapoffl/'
stats = extract_instagram_stats(insta_url)
if stats:
    followers, following, posts = stats
    print(f'Followers: {followers}')
    print(f'Following: {following}')
    print(f'Posts: {posts}')
else:
    print('Could not extract stats')


# Example usage
insta_url = 'https://www.instagram.com/santhoshprathapoffl/'
stats = extract_instagram_stats(insta_url)
if stats:
    followers, following, posts = stats
    print(f'Followers: {followers}')
    print(f'Following: {following}')
    print(f'Posts: {posts}')
else:
    print('Could not extract stats')


insta_url = 'https://www.instagram.com/manojithkrishnan/?hl=en'
username = extract_username_from_title(insta_url)
print(f'Username: {username}')
"""