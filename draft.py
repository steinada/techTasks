import threading
import time
import urllib.request


def sum_n(url):
    with urllib.request.urlopen(url) as u:
        print(url)
        return u.read()


start = time.time()
lock = threading.Lock()
urls = [
    'https://www.yandex.ru', 'https://www.google.com',
    'https://habrahabr.ru', 'https://www.python.org',
    'https://isocpp.org',
]
threads = [threading.Thread(target=sum_n, args=(url, )) for url in urls]


for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print('end')
print(time.time() - start)





