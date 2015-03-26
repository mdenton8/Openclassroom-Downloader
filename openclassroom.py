#!/usr/bin/env python

import itertools
from multiprocessing import Pool
import re
import os
import getpass
import errno
import urllib
from BeautifulSoup import BeautifulSoup


#COURSE_URL = 'http://openclassroom.stanford.edu/MainFolder/CoursePage.php?course=IntroToAlgorithms'

def make_sure_path_exists(path):
    print path
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def download_video(video_name, course_url, direc):
    make_sure_path_exists(os.getcwd()+ os.sep + direc + os.sep);
	
    if os.path.exists(os.getcwd()+ os.sep + direc + os.sep + video_name):
            print "Already downloaded", course_url
            return
	    
    course_name = course_url.split('course=')[1]
    request = urllib.urlopen('http://openclassroom.stanford.edu/MainFolder/'\
                             'courses/{0}/videos/{1}.xml'.format(course_name,
                                                                 video_name))
    response = request.read()

    flv_name = response.split('<videoFile>')[1].split('</videoFile>')[0]
    print 'Downloading: %s' % flv_name
    urllib.urlretrieve('http://openclassroom.stanford.edu/MainFolder/courses/'\
                       '{0}/videos/{1}'.format(course_name, flv_name),
                        os.getcwd()+ os.sep + direc + os.sep + flv_name)

def download_star(url_direc):
    download_video(*url_direc)

def main():
    course_url = raw_input('Enter course page URL: ')
    
    request = urllib.urlopen(course_url)
    response = request.read()
    soup = BeautifulSoup(response)

    direc = raw_input("Directory to store videos: ")

    results = soup.findAll('div', {'class': 'results-list'})
    names = []
    for result in results:
        lists = result.findAll('li')
        for li in lists:
            urls = li.findAll('a')
            for url in urls:
                video_name = str(url).split('video=')[1].split('&')[0]
                names.append(video_name)

    p = Pool(processes=10)
    p.map(download_star, itertools.izip(names, itertools.repeat(course_url), itertools.repeat(direc)))


if __name__ == '__main__':
    main()
