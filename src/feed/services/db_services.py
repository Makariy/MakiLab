from typing import BinaryIO, Tuple

from tortoise.exceptions import DoesNotExist

from lib.models import User
from src import get_config
from src.feed.models import *
from .remote_services import *


config = get_config()


async def get_feed_post_by_params(**params):
    """Returns feed post <src.feed.models.FeedPost> that suites the params.
    if feed post is not found, returns None"""
    try:
        return await FeedPost.get(**params)
    except DoesNotExist:
        return None


async def get_feed_post_image_by_params(**params):
    """Returns feed post image <src.feed.models.FeedPostImage> that suites the params.
    if feed post image is not found, returns None"""
    try:
        return await FeedPostImage.get(**params)
    except DoesNotExist:
        return None


async def get_feed_post_comment_by_params(**params):
    """Returns feed post comment <src.feed.models.FeedPostComment> that suites the params.
    if feed post comment is not found, returns None"""
    try:
        return await FeedPostComment.get(**params)
    except DoesNotExist:
        return None


async def get_feed_post_like_by_params(**params):
    """Returns feed post like <src.feed.models.FeedPostLike> that suites the params.
    if feed post like is not found, returns None"""
    try:
        return await FeedPostLike.get(**params)
    except DoesNotExist:
        return None


async def get_feed_post_likes_count(feed_post_id: int):
    """Returns post <src.feed.models.FeedPost> likes count"""
    post = await FeedPost.get(id=feed_post_id)
    return await post.likes.all().count()


async def get_feed_post_like_by_post_and_author(feed_post: FeedPost, like_author: User):
    """Returns post <src.feed.models.FeedPost> like which author is <like_author>,
    if like does not exist, returns None"""
    try:
        return await feed_post.likes.all().get(author=like_author)
    except DoesNotExist:
        return None


async def get_last_feed_posts(author_id: User, start_post_id: FeedPost = None, count=10):
    """Returns last <count> posts <src.feed.models.FeedPost> whose author_id is <author_id>
    starting after feed_post <start_feed>"""
    last_feed_posts = FeedPost.filter(author__id=author_id).order_by('-id').limit(count).select_related('author')
    if start_post_id:
        return await last_feed_posts.filter(id__lt=start_post_id)
    else:
        return await last_feed_posts


async def get_user_by_params(**params):
    """Returns user <src.feed.models.User> that suites the params,
    if user does not exist, returns None"""
    try:
        return await User.get(**params)
    except DoesNotExist:
        return None


"""
------------------------------------
        End getting objects
------------------------------------
"""


"""
------------------------------------
        Creating objects 
------------------------------------
"""


async def create_feed_post(author: User, text: str, images: Union[Tuple[FeedPostImage], None] = None):
    """Creates feed post <feed.models.FeedPost> with author <author>, text <text> and
    adds images <Tuple[feed.models.FeedPostImage]> if specified"""
    feed_post = FeedPost(author=author, text=text)
    await feed_post.save()

    if images:
        await feed_post.images.add(*images)
    return feed_post


async def create_feed_post_image(image_reader: BinaryIO):
    """Creates feed post image <feed.models.FeedPostImage> from image_reader"""
    feed_post_image = FeedPostImage()
    await feed_post_image.save()

    if not config.TESTING:
        return await save_feed_post_image_to_remote_server(image_reader, feed_post_image)

    return feed_post_image


async def create_feed_post_comment(comment_author: User, text: str):
    """Creates and returns feed post comment <feed.models.FeedPostComment> with text"""
    comment = FeedPostComment(author=comment_author, text=text)
    await comment.save()
    return comment


"""
------------------------------------
        End creating objects 
------------------------------------
"""



"""
------------------------------------
        Adding objects 
------------------------------------
"""


async def add_like_to_feed_post(post: FeedPost, like_author: User):
    """Adds like to the post <feed.models.FeedPost>"""
    if not await has_user_liked_feed_post(post, like_author):
        like = FeedPostLike(author=like_author)
        await like.save()
        await post.likes.add(like)
        await post.save()
        return True
    return False


async def add_comment_to_feed_post(post: FeedPost, comment: FeedPostComment):
    """Adds comment to the post <feed.models.FeedPost>"""
    await post.comments.add(comment)
    return comment


"""
------------------------------------
        End adding objects 
------------------------------------
"""


"""
------------------------------------
        Removing objects
------------------------------------
"""


async def remove_like_from_feed_post(post: FeedPost, like_author: User):
    """Removes like from post <feed.models.FeedPost>, if like exists,
    removes it from the post and returns True, else returns False"""
    like = await get_feed_post_like_by_post_and_author(post, like_author)
    if like:
        await post.likes.remove(like)
        return True
    else:
        return False


"""
------------------------------------
        Removing objects
------------------------------------
"""


"""
----------------------------------------
            Getting information         
----------------------------------------
"""


async def has_user_liked_feed_post(post: FeedPost, like_user: User):
    """If user had liked the post <feed.models.FeedPost>, returns True,
    else returns False"""
    like = await get_feed_post_like_by_post_and_author(post, like_user)
    if like:
        return True
    else:
        return False


"""
----------------------------------------
            Getting information         
----------------------------------------
"""


