import instaloader
import requests
from bs4 import BeautifulSoup
import cv2  
import urllib.request
import shutil
import os

ig = instaloader.Instaloader()
L = instaloader.Instaloader()
def ret_full_name(username):
    # Create an instance of Instaloader

    try:
        # Download the profile metadata
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Get the full name
        full_name = profile.full_name
        #print(full_name)
        return full_name
    except instaloader.exceptions.ProfileNotExistsException:
        #print(f"Profile '{username}' does not exist.")
        return None
    except Exception as e:
        #print(f"An error occurred: {e}")
        return None

def check_profile_privacy(username):
        
        profile = instaloader.Profile.from_username(ig.context, username)
        
        if profile.is_private:
            #print(f"The account {username} is private.")
            return 1
        else:
            #print(f"The account {username} is public.")
            return 0

def has_external_link_in_bio(username):
    # Create an instance of Instaloader

    try:
        # Download the profile metadata
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Get the bio text
        bio = profile.biography
        external_url = profile.external_url
        
        # Check if there's an external link in the bio or external URL field
        if external_url or ('http' in bio or 'https' in bio):
            return 1
        else:
            return 0
    except instaloader.exceptions.ProfileNotExistsException:
        #print(f"Profile '{username}' does not exist.")
        return 0
    except Exception as e:
        #print(f"An error occurred: {e}")
        return 0
    

def download_profile_pic(username):
        #ig = instaloader.Instaloader()
        ig.download_profile(username, profile_pic_only=True)

        # Move and rename the profile picture
        profile_pic_folder = username
        for file_name in os.listdir(profile_pic_folder):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                src_path = os.path.join(profile_pic_folder, file_name)
                dst_path = f"{username}{os.path.splitext(file_name)[1]}"
                shutil.move(src_path, dst_path)
                break

        # Clean up the directory created by Instaloader
        shutil.rmtree(profile_pic_folder)
        #print(f"Profile picture downloaded successfully for {username}")

def compare_images(username):
    # Read images
    download_profile_pic(username)
    image2_path = "test.jpg"
    image1_path = f"{username}.jpg"

    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    if image1 is None:
        return 0
    # Resize images to the same dimensions (256x256)
    common_size = (320,320)
    resized_image1 = cv2.resize(image1, common_size)
    resized_image2 = cv2.resize(image2, common_size)

    # Compute absolute difference
    difference = cv2.absdiff(resized_image1, resized_image2)
    # Sum of pixel differences
    sum_diff = difference.sum()
    
    if sum_diff == 0:
        print("No profile pic")
        return 0  # Images are the same
    else:
        #print("Profile pic exists")
        return 1  # Images are different
    if os.path.exists(image1_path):
        os.remove(image1_path)

def extract_info(username):
    # Create an instance of Instaloader
    #L = instaloader.Instaloader()

    try:
        # Retrieve profile information
        profile = instaloader.Profile.from_username(L.context, username)
        num_posts = profile.mediacount
        bio = profile.biography
        #print(f"The number of posts by {username} is: {num_posts}")

        #print(f"The bio is: {bio}")

        bio_length = len(bio)
        #print(f"The length of bio is: {bio_length}")
        return bio_length

        exturl = profile.external_url
        print(exturl)
    except instaloader.exceptions.ProfileNotExistsException:
        #print(f"Profile with username '{username}' does not exist.")
        return False
    except Exception as e:
        #print(f"An error occurred: {e}")
        return False
"""
if __name__ == "__main__":
    # Input Instagram username
    username = input("Enter the Instagram username: ")
    extract_info(username)
    download_profile_pic(username)
    compare_images(username)
    check_profile_privacy(username)
    """

