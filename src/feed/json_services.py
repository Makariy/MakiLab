from typing import Iterable
from .models import *


async def render_feed_post(feed_post: FeedPost) -> dict:
    """Returns a dictionary <dict> with a rendered feed post"""
    images_urls = []
    # if 0 < await feed_post.images.all().count():
    #    images_urls = [image.file_name for image in await feed_post.images.all()]

    # post_author = await feed_post.author

    return {
        'author': feed_post.author.username,
        'author_id':feed_post.author.id,
        'post_id': feed_post.id,
        'text': feed_post.text,
        'images_urls': images_urls,
        'date': feed_post.date.strftime('%d.%m.%Y %H:%M'),
    }


async def render_feed_posts(feed_posts: Iterable[FeedPost]):
    """Returns a dictionary <dict> with a rendered feed posts"""
    return {
        'feed_posts': [await render_feed_post(feed_post) for feed_post in feed_posts]
    }
