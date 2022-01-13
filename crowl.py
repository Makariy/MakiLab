import json
from crowler import get_videos_list, download_videos


if __name__ == '__main__':
    videos = get_videos_list()
    download_videos(videos['videos'])
 videos = json.loads(open('file.json', 'r').read())['videos']