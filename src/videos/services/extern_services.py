from src.videos.models import VideoPreview
from uuid import uuid4
import config
import os


async def create_preview(data: bytes) -> VideoPreview:
    uuid = uuid4()
    file_name = str(uuid)
    save_path = os.path.join(config.PREVIEW_SAVING_PATH, str(uuid))
    with open(save_path, 'wb') as file:
        file.write(data)
    return await VideoPreview.create(file_name=file_name)

