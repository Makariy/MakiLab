from typing import BinaryIO, Union
import requests

from src import get_config
from src.feed.models import FeedPostImage


config = get_config()


async def save_feed_post_image_to_remote_server(image_reader: BinaryIO, feed_post_image: FeedPostImage)\
        -> FeedPostImage:
    """Saves image to remote server. If the image is saved, returns <feed.models.FeedPostImage>
    instance with file name of this image on the remote server saved in it.
    If the image is NOT saved, raises a RuntimeError"""
    response = requests.post(
        url=f'{config.MEDIA_LOADER_URL}/upload',
        files={'file': image_reader},
        data={'file_id': feed_post_image.id}
    )
    status = response.json().get('status')
    if status and status == 'success':
        feed_post_image.file_name = response.json().get('file_name')
        await feed_post_image.save()
        return feed_post_image
    else:
        raise RuntimeError(f'Feed post image cannot be saved on remote server.\nReason: {response.json()}')


def delete_feed_post_image_from_remote_server(feed_post_image: FeedPostImage) -> None:
    """Deletes image from remote server. If the image is not removed, raises RuntimeError"""
    response = requests.post(
        url=f'{config.MEDIA_LOADER_URL}/delete',
        data={'file_name': feed_post_image.file_name}
    )
    status = response.json().get('status')
    if status and status == 'success':
        return
    else:
        raise RuntimeError(f'Feed post image cannot be deleted from remote server.\nReason: {response.json()}')
