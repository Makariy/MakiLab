from typing import Iterable
from .models import *


async def render_feed_post(feed_post: FeedPost) -> dict:
    """Returns a dictionary <dict> with a rendered feed post"""
    images_urls = []
    comments = []
    
    if 0 < len(feed_post.images):
        images_urls = [image.file_name for image in feed_post.images]
    if 0 < len(feed_post.comments):
        comments = [{'author_id': comment.author.id, 'text': comment.text} for comment in feed_post.comments]

    return {
        'author': feed_post.author.username,
        'author_id': feed_post.author.id,
        'post_id': feed_post.id,
        'text': feed_post.text,
        'images_urls': images_urls,
        'comments': comments,
        'date': feed_post.date.strftime('%d.%m.%Y %H:%M'),
    }


async def render_feed_posts(feed_posts: Iterable[FeedPost]):
    """Returns a dictionary <dict> with a rendered feed posts"""
    return {
        'feed_posts': [await render_feed_post(feed_post) for feed_post in feed_posts]
    }
