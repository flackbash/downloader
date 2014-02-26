from urllib.request import urlopen, urlretrieve
import re
import os
import time


def extract_links(url, pattern):
    """Extracts all links of files with a specified pattern from a website

    Arguments:
    url -- a string representing an url
    pattern -- a string representing a file extension
    """
    source = urlopen(url)
    sourcecode = source.readlines()
    source.close()
    links = []
    #get a list of links
    for line in sourcecode:
        new_link = re.findall(r'<a\s+href="(.+?\.%s)">.*?</a>' % pattern, str(line))
        if new_link:
            links += (new_link)
    return links


def download_files(url, directory=os.getcwd(), pattern='pdf', number=None, overwrite=False):
    """Downloads all files from a website. Doesn't work with funny hyperlinks.

    Arguments:
    url -- a string representing an url
    directory -- a string representing the directory in which all downloaded files will be saved
    pattern -- a string: all files with this file extension will be downloaded
    number -- an integer: up to 'number' files will be downloaded
    """
    t0 = time.time()
    count = 0
    count_fails = 0
    count_skip = 0
    links = extract_links(url, pattern)
    if not links:
        print('No files detected.')
    #prepare a string to get the file url (cut off last bit)
    url_end = url.split('/')[-1]
    url_string = url.replace(url_end, '')
    for lnk in links[:number]:
        try:
            filename = lnk.rpartition('/')[-1]
            #skip existing files if overwrite == False
            if not overwrite and filename in os.listdir(directory):
                print("skipped %s" % filename)
                count_skip += 1
                continue
            #download files
            urlretrieve(url_string + lnk, os.path.join(directory, filename))
            print("downloaded %s" % filename)
            count += 1
        except:
            print("%s: download failed" % filename)
            count_fails += 1
    tdelta = time.time() - t0
    print('*' * 38, '\nFinished: %2d downloads in %.1f seconds.' % (count, tdelta))
    print('%12d downloads failed.' % count_fails)
    print('%12d files skipped.\n' % count_skip)


#download_files('http://www.informatik.uni-freiburg.de/~ki/teaching/ws1314/info1/lecture_de.html', number=4)
