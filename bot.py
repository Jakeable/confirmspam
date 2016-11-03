import praw
import time
import os

subreddit = str(os.environ.get('subreddit'))
r = praw.Reddit(user_agent='/r/{0} spamfilter autospammer by /u/Jakeable'.format(subreddit),
                client_id=str(os.environ.get('client_id')),
                client_secret=str(os.environ.get('client_secret')),
                username=str(os.environ.get('username')),
                password=str(os.environ.get('password')))


sub = r.subreddit(subreddit)

def check_modqueue():
    content = r.get("/r/" + subreddit + "/about/modqueue", {"only":"comments"})
    for item in content:
        if item.banned_by == "true" or item.banned_by == True: # not sure how praw interprets "true" from reddit
             sub.mod.remove(item) # confirm remove
        elif str(item.distinguished).lower() == 'moderator':
            sub.mod.approve(item) # approve distinguished comments

if __name__ == '__main__':
    while True:
        check_modqueue()
        time.sleep(60)

