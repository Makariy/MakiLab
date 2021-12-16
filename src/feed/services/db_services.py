from src.feed.models import *
from tortoise.exceptions import DoesNotExist


def get_feed_post_by_params(**params):
    """Returns feed post <src.feed.models.FeedPost> that suites the params.
    if feed post is not found, returns None"""
    try:
        return await FeedPost.get(**params)
    except DoesNotExist:
        return None


def get_feed_post_image_by_params(**params):
    """Returns feed post image <src.feed.models.FeedPostImage> that suites the params.
    if feed post image is not found, returns None"""
    try:
        return await FeedPostImage.get(**params)
    except DoesNotExist:
        return None


def get_feed_post_comment_by_params(**params):
    """Returns feed post comment <src.feed.models.FeedPostComment> that suites the params.
    if feed post comment is not found, returns None"""
    try:
        return await FeedPostComment.get(**params)
    except DoesNotExist:
        return None


def get_feed_post_like_by_params(**params):
    """Returns feed post like <src.feed.models.FeedPostLike> that suites the params.
    if feed post like is not found, returns None"""
    try:
        return await FeedPostLike.get(**params)
    except DoesNotExist:
        return None


def get_feed_post_likes_count(feed_post_id: int):
    """Returns post <src.feed.models.FeedPost> likes count"""
    post = await FeedPost.get(id=feed_post_id)
    return post.likes.all().count()


def get_feed_post_like_by_post_and_author(feed_post: FeedPost, like_author: User):
    """Returns post <src.feed.models.FeedPost> like which author is <like_author>,
    if like does not exist, returns None"""
    try:
        return feed_post.likes.get(author=like_author)
    except DoesNotExist:
        return None


def get_last_feed_posts(author_id: User, start_post_id: FeedPost = None, count=10):
    """Returns last <count> posts <src.feed.models.FeedPost> whose author_id is <author_id>
    starting after feed_post <start_feed>"""
    last_feed_posts = FeedPost.filter(author__id=author_id).order_by('-id')
    if start_post_id:
        return last_feed_posts.filter(id__lt=start_post_id)[:count]
    else:
        return last_feed_posts[:count]


def get_user_by_params(**params):
    """Returns user <src.feed.models.User> that suites the params,
    if user does not exist, returns None"""
    try:
        return User.get(**params)
    except DoesNotExist:
        return None

