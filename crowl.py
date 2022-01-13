from crowler import get_videos_list, download_videos, Paginator, Proxier


url = 'https://xvideos.com'


def start():
    global url
    paginator = Paginator(url)
    proxier = Proxier()
    try:
        for url in paginator.get_urls_iter():
            videos = get_videos_list(url)
            download_videos(videos['videos'], proxier)
    except:
        # Save used proxies
        del proxier


if __name__ == '__main__':
    start()
