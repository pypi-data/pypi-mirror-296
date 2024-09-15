import urllib3
from hashlib import md5

class Library:
    @staticmethod
    def is_live(url):
        http = urllib3.PoolManager()
        response = http.request('HEAD', url)

        return 200 <= response.status < 400

    @staticmethod
    def body_md5(url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)

        return md5(response.data).hexdigest()
