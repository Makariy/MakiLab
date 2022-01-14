from crowler.crowl import download_videos, get_videos_list
from crowler.lib.proxier import Proxier
from crowler.lib.paginator import Paginator


url = 'https://xvideos.com'


def start():
    global url
    paginator = Paginator(url)
    proxier = Proxier()
    for url in paginator.get_urls_iter():
        videos = get_videos_list(url)
        download_videos(videos, proxier)
    # Save used proxies
    del proxier



