from urllib.request import urlopen, urlretrieve
import re
import os
import time


def download_files(url, directory=os.getcwd(), pattern='pdf', number=None):
    """Downloads all files from a website. Doesn't work with funny hyperlinks.

    Arguments:
    url -- a string representing an url
    directory -- a string representing the directory in which all downloaded files will be saved
    pattern -- a string: all files with this file ending will be downloaded (hopefully)
    number -- an integer: up to number files will be downloaded
    """
    t0 = time.time()
    source = urlopen(url)
    sourcecode = source.readlines()
    source.close()
    links = []
    #get a list of links
    for line in sourcecode:
        new_link = re.findall(r'<a\s+href="(.+?\.%s)">.*?</a>' % pattern, str(line))
        if new_link:
            links += (new_link)
    #prepare a string to get the file url (cut off last bit)
    url_end = url.split('/')[-1]
    url_string = url.replace(url_end, '')
    count = 0
    count_fails = 0
    if not links:
        print('No files detected.')
    #download files
    for lnk in links[:number]:
        try:
            filename = lnk.rpartition('/')[-1]
            urlretrieve(url_string + lnk, os.path.join(directory, filename))
            print("downloaded %s" % filename)
            count += 1
        except:
            print("%s: download failed" % filename)
            count_fails += 1
    tdelta = time.time() - t0
    print('*' * 38, '\nFinished: %2d downloads in %.1f seconds.\n %11d downloads failed.\n' % (count, tdelta, count_fails))
