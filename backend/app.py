import pandas as pd
import numpy as np
#from tld import get_tld
from urllib.parse import urlparse
from urlcapture import * 
from instacapture import *
import re
import joblib 
import sys
import json
import locale
import sys, os
locale.setlocale(locale.LC_ALL, '')
# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

classifier = open('instagram_fake_classifier.pkl','rb')
model = joblib.load(classifier)

def num_compute(num):
    if num[-1] == 'K':
        return locale.atof(num[:-1])*1e3
    elif num[-1] == 'M':
        return locale.atof(num[:-1])*1e6
    else:
        return locale.atof(num)
    
def process_input(username,followers,following,posts):
    df={'username':[username]}
    data=pd.DataFrame(df,columns=['username','profile pic', 'nums/length username', 'fullname words',
       'nums/length fullname', 'name==username', 'description length',
       'external URL', 'private', '#posts', '#followers', '#follows'])
    data['profile pic'] = (data['username'].apply(lambda x:  compare_images(x)))
    data['nums/length username'] = (data['username'].apply(lambda x:  count_numerical_characters(x)/(len(x)+1)))
    fname = str(ret_full_name(username))
    data['fullname words'] = (data['username'].apply(lambda x:  len(fname.split())))
    data['nums/length fullname'] = (data['username'].apply(lambda x:  count_numerical_characters(fname)/(len(fname)+1)))
    data['name==username'] = (data['username'].apply(lambda x: (x == ret_full_name(x))))
    data['description length'] = (data['username'].apply(lambda x:  (extract_info(x))))
    data['external URL'] = (data['username'].apply(lambda x:  has_external_link_in_bio(x)))
    data['private'] = (data['username'].apply(lambda x:  check_profile_privacy(x)))
    data['#posts'] = data['username'].apply(lambda x:  num_compute(posts)+1)
    data['#followers'] = data['username'].apply(lambda x:  num_compute(followers)+1)
    data['#follows'] = data['username'].apply(lambda x:  num_compute(following)+1)
    data = data.drop('username',axis=1)
    #data.info()
    return data

def count_numerical_characters(s):
    count = 0
    for char in s:
        if char.isdigit():
            count += 1
    return count

def classify_url(url,followers,following, posts):
    data=process_input(url,followers,following, posts)
    pred=model.predict(data)
    prob = model.predict_proba(data)
    if pred == 1:
        confidences= prob.max(axis=1)
    else:
        confidences= prob.min(axis=1)
    return pred, (confidences*10)[0]

if __name__ == '__main__':
    blockPrint()
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    #url = 'https://www.instagram.com/gal_gadot/'
    username = extract_username_from_title(url)
    #print(username)
    #print(ret_full_name(username))
    #print(len(ret_full_name(username).split()))
    followers,following, posts = extract_instagram_stats(url)
    result, score = classify_url(username, followers,following, posts)
    res=result.tolist()
    res.append(score)
    enablePrint()
    print(res[0]," ",round(res[1],1))
    #print(json.dumps(res))