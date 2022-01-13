

class Paginator:
    def __init__(self, url):
        self.counter = 1
        self.base_url = url + '/new/'

    def get_urls_iter(self):
        for i in range(1000):
            yield self.base_url + str(self.counter)
            self.counter += 1
