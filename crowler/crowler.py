import asyncio
from typing import List, Dict
from .lib.video_list_parser import VideoListParser
from .lib.video_page_parser import VideoPageParser
from .lib.proxier import Proxier
from .lib.paginator import Paginator


root = 'https://xvideos.com'


def get_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    return loop


def get_videos_list(url='https://xvideos.com'):
    loop = get_loop()
    parser = VideoListParser(url)
    return loop.run_until_complete(parser.get_videos_rendered())


def download_videos(videos: List[Dict[str, str]], proxier: Proxier):
    proxies = proxier.get_proxies()
    proxies_count = len(proxies)

    loop = get_loop()

    for i in range(0, len(videos), proxies_count):
        tasks = []

        videos_set = videos[i:i+proxies_count]
        for x in range(len(videos_set)):
            video = videos_set[x]

            # Video url: "/asdonsadsa/23/123/51/asdpsadmpsad_sadkasd_asdasd"
            # root: https://xvideos.com
            video['url'] = root + video['url']
            parser = VideoPageParser()
            tasks.append(parser.download_video(video, proxies[x], '/home/makariy/disk/data/'))

        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        # Change proxies if not working)))
        #     ^      ^
        #      _ 00 _
        #      <---->
        except RuntimeError:
            for proxy in proxies:
                proxier.add_used_proxy(proxy)
                proxier.make_proxies()
                proxies = [proxier.get_proxy() for i in range(8)]
