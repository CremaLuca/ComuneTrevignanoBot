import env_file
from facebook_scraper import get_posts
from tinydb import Query, TinyDB

import telegram

MAX_TELEGRAM_MSG_LEN = 900

# initialization
envs = env_file.get()
db = TinyDB('./db.json')

page_name = envs['PAGE_NAME']


def get_new_posts():
    '''
    Retrieves the last 2 pages of posts and checks if there is are new posts (not already in DB).
    If new posts are found they're returned with newest at the bottom.
    '''
    new_posts = list()
    Post = Query()  # Database Post object

    # Retrieve last 2 pages of posts
    facebook_posts = get_posts(page_name, pages=2)
    if(len(facebook_posts) <= 0):
        print("Couldn't retrieve any new post")
        return list()

    for post in facebook_posts:
        # Check if it has already been posted
        if(len(db.search(Post.post_id == post['post_id'])) == 0):
            new_posts.append(post)

    return list(reversed(new_posts))


def message_new_posts():
    # Retrieve new posts
    new_posts = get_new_posts()

    if(len(new_posts) <= 0):
        print("There aren't any new posts")
        return
    # Send messages
    for post in new_posts:
        # Preprocess message
        post['text'] = telegram.escape_text(shorten_text(post['text']))
        if len(post['text']) > 0:
            post['text'] += "\n\n"  # "Read on facebook" spacing only if there is some text
        post['text'] += "🔎  [Leggi su Facebook]({})".format(post['post_url'])
        # Send message
        if('images' in post):
            telegram.send_photos_url(post['text'], post['images'])
        # elif('video' in post):
        #    pass
        elif('image' in post):
            telegram.send_photo_url(post['text'], post['image'])
        else:
            telegram.send_message(post['text'])

    # Update post db so that new posts are not re-posted
    for post in new_posts:
        db.insert({'post_id': post['post_id']})
        print("inserted post {} in db".format(post['post_id']))


def shorten_text(text):
    '''
    Returns an ellipsed text if it exceeddes MAX_TELEGRAM_MSG_LEN.
    '''
    if(len(text) > MAX_TELEGRAM_MSG_LEN):
        text = text[:MAX_TELEGRAM_MSG_LEN] + "..."
    return text


if __name__ == "__main__":
    print("Checking for new posts...")
    message_new_posts()
    print("Done!")
