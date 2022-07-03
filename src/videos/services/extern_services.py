from uuid import uuid4
from src import config
import os


async def create_preview(data: bytes) -> str:
    uuid = uuid4()
    file_name = str(uuid)
    save_path = os.path.join(config.PREVIEW_SAVING_PATH, str(uuid))
    with open(save_path, 'wb') as file:
        file.write(data)
    return file_name
