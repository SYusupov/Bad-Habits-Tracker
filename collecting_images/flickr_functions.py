import flickrapi
import os
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
import multiprocessing
from functools import partial

# TO DO: delete these keys if sharing on github
flickr_key = "b4d346de26f02a9ae3ff4b1c97cd4109"
flickr_secret = "973096aa6cfba641"

flickr = flickrapi.FlickrAPI(flickr_key, flickr_secret, format='parsed-json')

def flickr_url(photo, size=''):
    url = 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}{size}.jpg'
    if size:
        size = '_' + size
    return url.format(size=size, **photo)

def fetch_photo(dir_name, photo):
    urlretrieve(flickr_url(photo), os.path.join(dir_name, photo['id'] + '.jpg'))

def fetch_image_set(query, dir_name=None, count=250, sort='relevance'):
    res = flickr.photos.search(text='"{}"'.format(query), 
                               per_page=count, sort=sort)['photos']['photo']
    dir_name = dir_name or query
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with multiprocessing.Pool() as p:
        p.map(partial(fetch_photo, dir_name), res)