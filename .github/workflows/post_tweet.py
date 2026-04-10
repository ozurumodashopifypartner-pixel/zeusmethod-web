#!/usr/bin/env python3
"""
GitHub Actions Tweet Poster
Posts scheduled tweets for Focus Forward
"""

import os
import requests
import urllib.parse
import hmac
import hashlib
import time
import random
import base64
from datetime import datetime

# Get credentials from environment variables
API_KEY = os.environ.get('API_KEY', '')
API_SECRET = os.environ.get('API_SECRET', '')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', '')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', '')

def create_oauth_header(method, url, params=None):
    timestamp = str(int(time.time()))
    nonce = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
    
    oauth_params = {
        'oauth_consumer_key': API_KEY,
        'oauth_nonce': nonce,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': timestamp,
        'oauth_token': ACCESS_TOKEN,
        'oauth_version': '1.0'
    }
    
    if params:
        oauth_params.update(params)
    
    param_string = '&'.join([f'{urllib.parse.quote(k, safe="")}={urllib.parse.quote(str(v), safe="")}' 
                            for k, v in sorted(oauth_params.items())])
    base_string = '&'.join([
        method.upper(),
        urllib.parse.quote(url, safe=''),
        urllib.parse.quote(param_string, safe='')
    ])
    
    signing_key = f'{urllib.parse.quote(API_SECRET)}&{urllib.parse.quote(ACCESS_TOKEN_SECRET)}'
    signature = hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
    oauth_params['oauth_signature'] = base64.b64encode(signature).decode()
    
    return 'OAuth ' + ', '.join([f'{k}="{urllib.parse.quote(v, safe="")}"' 
                                for k, v in oauth_params.items()])

def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {
        'Authorization': create_oauth_header('POST', url),
        'Content-Type': 'application/json'
    }
    payload = {'text': text}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 201:
            return response.json()['data']['id']
        else:
            print(f"❌ Error {response.status_code}: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return None

# Tweet library - organized by day of week
TWEETS = {
    'friday': [
        "Friday energy for ADHD twitter 🎉 You made it through another week. Whether you crushed goals or just survived—both count. #ADHD",
        "ADHD confession: I have 47 browser tabs open. I need all of them. I will close none. This is my life. Who relates? 😅 #ADHD",
        "Reminder: You are not wasting potential. You are learning to work WITH your brain in a world built for neurotypical minds. #ADHD",
        "The ADHD to-do list: Important thing, other important thing, reply to email, [4 hours researching random topic], oh no it is midnight. #ADHD",
        "Micro-wins for ADHD: Brushed teeth, took meds, made breakfast, sent email. If you did any of these today—you are winning. #ADHD",
        "Executive dysfunction is not laziness. It is a neurological barrier. The solution is not willpower—it is lowering the barrier. #ADHD",
        "Weekend plans for ADHDers: Saturday hyperfocus until 3 AM, Sunday exhausted doing nothing, Monday wonder why weekends do not recharge. #ADHD",
        "Better weekend plan: Schedule actual rest, one fun thing, body doubling for admin tasks, prep for Monday. Rest is productive too. #ADHD",
        "Friday night ADHD: I should start a new project, learn a skill, reorganize life. I will scroll TikTok 5 hours, feel guilty. Who else? 🙋‍♂️ #ADHD",
        "Goodnight ADHD twitter 🌙 Whatever you did today—you are still worthy, still enough, still making progress. Sleep well. 💤 #ADHD"
    ],
    'saturday': [
        "Saturday ADHD energy: Hyperfocus on new hobby for 6 hours, abandon it forever, find new hobby, repeat. #ADHD",
        "Weekend productivity guilt is real. But rest IS productive. Your brain needs downtime to function. #ADHD",
        "ADHD weekend tip: Body doubling works on weekends too. Find a virtual co-working session. #ADHD",
        "Saturday confession: I planned to be productive. I have done nothing. And that is okay. #ADHD",
        "The ADHD weekend cycle: Big plans → Small execution → Guilt → Recovery. Who can relate? #ADHD",
        "Sunday scaries hit different with ADHD. The whole weekend feels like it disappeared. #ADHD",
        "Weekend wins count too: Showered, ate, rested. That is enough. #ADHD",
        "ADHD hack for weekends: Do ONE thing you actually want to do. Not productive. Just fun. #ADHD",
        "Saturday night: Time to hyperfocus on a Wikipedia rabbit hole at 2 AM. #ADHD",
        "Rest is not lazy. It is necessary. Especially for brains that work overtime. #ADHD"
    ],
    'sunday': [
        "Sunday scaries check: Who else feeling that pre-Monday anxiety? 🙋‍♂️ #ADHD",
        "Sunday prep tip: Spend 10 minutes planning Monday. Reduces morning panic. #ADHD",
        "The Sunday ADHD paradox: Too much weekend left to start something new, too little to actually do it. #ADHD",
        "Restful Sunday = productive week. Stop feeling guilty about doing nothing. #ADHD",
        "ADHD Sunday routine: Panic about Monday, try to do everything, accomplish nothing, panic more. #ADHD",
        "Sunday reminder: You survived last week. You will survive next week too. #ADHD",
        "Body doubling on Sunday evenings = Monday prep without the overwhelm. #ADHD",
        "Sunday night thoughts: Did I forget something important all weekend? Probably. #ADHD",
        "New week, new chance to work WITH your brain. Not against it. #ADHD",
        "Sunday checklist: Rest ✓ Eat ✓ Sleep. That is enough preparation for Monday. #ADHD"
    ],
    'monday': [
        "Monday morning ADHD: Where did the weekend go? What am I doing? Who am I? #ADHD",
        "Monday reminder: Start small. One tiny task. Momentum builds from there. #ADHD",
        "The Monday dopamine crash is real. Be gentle with yourself today. #ADHD",
        "ADHD Monday hack: Do the interesting task first. Boring stuff comes after momentum. #ADHD",
        "Monday confession: I have no idea what I am doing but I am doing it anyway. #ADHD",
        "New week, same brain. Work WITH it, not against it. #ADHD",
        "Monday micro-win: Opened laptop. That counts. Next task: Open document. #ADHD",
        "ADHD energy Monday morning: Either hyperfocused or completely frozen. No in between. #ADHD",
        "Monday mindset: Progress over perfection. Done over perfect. #ADHD",
        "You survived Monday. That is the win. Everything else is bonus. #ADHD"
    ],
    'tuesday': [
        "Tuesday: The forgotten day. Monday energy is gone, Friday is too far. #ADHD",
        "Tuesday tip: Time to check in on those Monday goals. Adjust as needed. No shame. #ADHD",
        "ADHD Tuesday reality: Forgot what I was working on. Starting something new instead. #ADHD",
        "Tuesday motivation: You made it through Monday. You can make it through today. #ADHD",
        "The Tuesday slump is real. Try a dopamine menu to get through. #ADHD",
        "Tuesday check-in: One task done = success. Everything else is extra. #ADHD",
        "ADHD Tuesday energy: Hyperfocused on wrong thing, ignoring priorities. Classic. #ADHD",
        "Tuesday reminder: Interest-based scheduling. Do what energizes you today. #ADHD",
        "Midweek momentum: You are closer to Friday than you think. #ADHD",
        "Tuesday win: Showed up. That is enough. #ADHD"
    ],
    'wednesday': [
        "Wednesday: Hump day for neurotypicals, just another day for ADHD. #ADHD",
        "Midweek check: How is your energy? Adjust expectations accordingly. #ADHD",
        "Wednesday ADHD tip: Body doubling session to get through the midweek slump. #ADHD",
        "Wednesday confession: Forgot what day it is. Thought it was Tuesday. Or Thursday. #ADHD",
        "Halfway through the week. You are doing better than you think. #ADHD",
        "Wednesday energy audit: What is draining you? What is energizing you? Adjust. #ADHD",
        "ADHD Wednesday: Too much week left, not enough dopamine. #ADHD",
        "Wednesday reminder: One good hour of work > eight distracted hours. Quality over quantity. #ADHD",
        "Midweek micro-win: Did something, anything. Counts. #ADHD",
        "Wednesday mindset: Keep going. Weekend is closer than Monday now. #ADHD"
    ],
    'thursday': [
        "Thursday: Almost Friday energy. Hold on. #ADHD",
        "Thursday tip: Prep for Friday now. Reduces tomorrow morning chaos. #ADHD",
        "ADHD Thursday reality: Hyperfocused all week, now exhausted. Pushing through. #ADHD",
        "Thursday motivation: One more day. You have survived harder weeks. #ADHD",
        "The Thursday evening wind-down starts... never. ADHD brain says keep going. #ADHD",
        "Thursday check-in: What can you delegate, delete, or defer before Friday? #ADHD",
        "ADHD Thursday: Started 10 things this week, finished 0. Starting 3 more today. #ADHD",
        "Thursday reminder: Rest is coming. Push through today. #ADHD",
        "Almost Friday energy: Mismatched enthusiasm for weekend plans. #ADHD",
        "Thursday win: Almost made it through the week. That is the victory. #ADHD"
    ]
}

def get_today_tweets():
    """Get tweets for today based on day of week"""
    day = datetime.now().strftime('%A').lower()
    return TWEETS.get(day, TWEETS['friday'])

def get_tweet_index():
    """Get which tweet to post based on current hour"""
    hour = datetime.now().hour
    
    # Map hours to tweet indices (0-9 for 10 tweets/day)
    time_map = {
        10: 0,  # 6 AM EST
        12: 1,  # 8 AM EST
        14: 2,  # 10 AM EST
        16: 3,  # 12 PM EST
        18: 4,  # 2 PM EST
        20: 5,  # 4 PM EST
        22: 6,  # 6 PM EST
        0: 7,   # 8 PM EST (next day UTC)
        2: 8,   # 10 PM EST
        3: 9    # 11:30 PM EST
    }
    
    return time_map.get(hour, 0)

def main():
    print(f"🐦 GitHub Actions Tweet Poster")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 50)
    
    # Check credentials
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("❌ Missing Twitter API credentials")
        print("   Set secrets in GitHub repo settings")
        return
    
    # Get tweets for today
    today_tweets = get_today_tweets()
    
    # Get which tweet to post
    tweet_index = get_tweet_index()
    
    if tweet_index >= len(today_tweets):
        print(f"⚠️ Tweet index {tweet_index} out of range")
        return
    
    tweet_text = today_tweets[tweet_index]
    
    print(f"📤 Posting tweet {tweet_index + 1}/10")
    print(f"📝 {tweet_text[:60]}...")
    print()
    
    # Post the tweet
    tweet_id = post_tweet(tweet_text)
    
    if tweet_id:
        print(f"✅ SUCCESS! ID: {tweet_id}")
        print(f"🔗 https://twitter.com/zeus_method/status/{tweet_id}")
    else:
        print(f"❌ FAILED to post tweet")

if __name__ == "__main__":
    main()