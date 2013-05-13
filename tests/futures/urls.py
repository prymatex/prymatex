from concurrent import futures
import urllib.request, urllib.error, urllib.parse

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

def load_url(url, timeout):
    return urllib.request.urlopen(url, timeout=timeout).read()

def url_loaded(future):
    try:
        future.result()
    except Exception as e:
        print(e)
    
with futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = [executor.submit(load_url, url, 60) for url in URLS ]

    print("vos manejate")
    for future in future_to_url:
        future.add_done_callback(url_loaded)
    print("nosotros continuamos por aca")