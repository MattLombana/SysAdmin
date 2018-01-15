#! /usr/bin/env python3

# Script to automatically download all VMs from https://www.vulnhub.com/

import logging
import math
import os
import requests
import sys
import time
import urllib.request
from bs4 import BeautifulSoup

DOWNLOAD_DIR = "/mnt/Archive/Vulnhub"
BASE_URL = 'https://www.vulnhub.com'
VMS_PER_PAGE = 10


def is_number(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = min(int(count * block_size * 100 / total_size), 100)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def download_file(filename, url):
    print('')
    print(filename)
    urllib.request.urlretrieve(url, filename, reporthook)
    print('')


def get_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def get_num_pages(url):
    soup = get_page(url)
    return int(soup.find('div', {'class': 'text-center pagination'}).findAll('li')[-2].text)


def get_page_vms(page_url):
    """
    Gets the url for each vm displayed on the page page_url
    """
    vms = []
    page = get_page(page_url)
    for title in page.findAll('div', {'class': 'span9 entry-title'}):
        a = title.find('a')
        vm_url = BASE_URL + a['href']
        vm_name = a.text.replace('/', '-')
        vm_num = vm_url.split(',')[-1].replace('/', '')
        if is_number(vm_num):
            vm_num = vm_num.zfill(3)
        else:
            vm_num = '000'

        vms.append((vm_name, vm_url, vm_num))
    return vms


def get_vm_release(soup):
    description = ''
    try:
        for li in soup.find(id='release').findAll('li'):
            if li.find('a'):
                description += (li.text + ' (' + BASE_URL + li.find('a')['href'] + ')')
            else:
                description += li.text
            description += '\n'
        return description
    except:
        return description


def get_vm_download(soup):
    description = ''
    try:
        for li in soup.find(id='download').findAll('li'):
            if li.find('a'):
                description += (li.text + ' (' + BASE_URL + li.find('a')['href'] + ')')
            else:
                description += li.text
            description += '\n'
        return description
    except:
        return description


def get_vm_description(soup):
    description = ''
    try:
        for p in soup.find(id='description').findAll('p'):
            if p.find('a'):
                description += (p.text + ' (' + BASE_URL + p.find('a')['href'] + ')')
            else:
                description += p.text
            description += '\n\n'
        return description
    except:
        return description


def get_vm_file_info(soup):
    description = ''
    try:
        for li in soup.find(id='fileinfo').findAll('li'):
            if li.find('a'):
                description += (li.text + ' (' + BASE_URL + li.find('a')['href'] + ')')
            else:
                description += li.text
            description += '\n'
        return description
    except:
        return description


def get_vm_hoster(soup):
    description = ''
    try:
        for li in soup.find(id='vm').findAll('li'):
            if li.find('a'):
                description += (li.text + ' (' + BASE_URL + li.find('a')['href'] + ')')
            else:
                description += li.text
            description += '\n'
        return description
    except:
        return description


def get_vm_networking(soup):
    description = ''
    try:
        for li in soup.find(id='networking').findAll('li'):
            if li.find('a'):
                description += (li.text + ' (' + BASE_URL + li.find('a')['href'] + ')')
            else:
                description += li.text
            description += '\n'
        return description
    except:
        return description


def get_vm_download_url(soup):
    return list(map((lambda x: x.find('a')['href']), soup.find(id='download').findAll('li')))[0]


def get_vm_screenshots(soup):
    screenshots = []
    try:
        for screenshot in soup.find(id='screenshot').findAll('a'):
            src = screenshot['href']
            name = screenshot['href'].split('/')[-1].replace('/', '-')
            screenshots.append((name, BASE_URL + src))
        return screenshots
    except:
        return screenshots


def get_vm_info(name, vm_url):
    soup = get_page(vm_url)

    release = get_vm_release(soup)
    download = get_vm_download(soup)
    description = get_vm_description(soup)
    file_info = get_vm_file_info(soup)
    hoster = get_vm_hoster(soup)
    networking = get_vm_networking(soup)
    download_url = get_vm_download_url(soup)
    screenshots = get_vm_screenshots(soup)

    return {'name': name,
            'release': release,
            'download': download,
            'description': description,
            'file_info': file_info,
            'hoster': hoster,
            'networking': networking,
            'download_url': download_url,
            'screenshots': screenshots}


def write_vm_info_file(directory, filename, info):
    with open(os.path.join(directory, filename), 'a+') as f:
        f.write('# Name: {}\n'.format(info['name']))
        f.write('\n\n')

        f.write('## Release\n')
        f.write(info['release'])
        f.write('\n\n')

        f.write('## Download\n')
        f.write(info['download'])
        f.write('\n\n')

        f.write('## Description\n')
        f.write(info['description'])
        f.write('\n\n')

        f.write('## File Info\n')
        f.write(info['file_info'])
        f.write('\n\n')

        f.write('## Hoster\n')
        f.write(info['hoster'])
        f.write('\n\n')

        f.write('## Networking\n')
        f.write(info['networking'])
        f.write('\n\n')

        f.write('## Download URL: {}\n'.format(info['download_url']))


def download_vm_screenshots(vm_directory, vm_info):
    screenshot_directory = os.path.join(vm_directory, 'screenshots')

    if not os.path.exists(screenshot_directory):
        os.mkdir(screenshot_directory)

    for filename, url in vm_info['screenshots']:
        download_file(os.path.join(screenshot_directory, filename), url)


def download_vm(vm_name, url, num):
    logging.info('Starting to download {}'.format(vm_name))

    vm_info = get_vm_info(vm_name, url)

    vm_directory = os.path.join(DOWNLOAD_DIR, '{} - {}'.format(num, vm_name))

    if not os.path.exists(vm_directory):
        os.mkdir(vm_directory)

    write_vm_info_file(vm_directory, vm_name, vm_info)

    logging.debug('Downloading screenshots for {}'.format(vm_name))
    download_vm_screenshots(vm_directory, vm_info)
    logging.debug('Downloaded screenshots for {}'.format(vm_name))

    logging.debug('Starting to download the vm for {}'.format(vm_name))
    download_name = vm_info['download_url'].split('/')[-1].replace('/', '-')
    download_file(os.path.join(vm_directory, download_name), vm_info['download_url'])
    logging.debug('Finished downloading the vm for {}'.format(vm_name))

    logging.info('Finished downloading {}'.format(vm_name))
    logging.info('\n')




def main():
    # Set up logging to a file
    logging.basicConfig(filename=(os.path.join(DOWNLOAD_DIR, 'log_file.log')), level=logging.DEBUG)

    # Set up urllib headers
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')]
    urllib.request.install_opener(opener)

    # Accumulator to keep track of the urls for all vms
    all_urls = []

    # Get total number of pages
    num_pages = get_num_pages(BASE_URL)

    # Find the most recent vm downloaded
    latest_vm = 0
    most_recent_file = os.path.join(DOWNLOAD_DIR, 'most_recent')
    if os.path.isfile(most_recent_file):
        try:
            with open(most_recent_file, 'r') as f:
                latest_vm = int(f.readline())
        except:
            latest_vm = 0

    # find the largest page that needs to be checked
    largest_page = math.ceil((num_pages + 1) - (latest_vm / VMS_PER_PAGE))
    if largest_page > num_pages:
        largest_page = num_pages

    # for each page in range 1..largest_page
    for page in range(1, largest_page + 1):
        # get list of urls on that page, and add it to the running total
        all_urls += get_page_vms(BASE_URL + '/?page=' + str(page))

    largest_downloaded = latest_vm

    for name, url, number_s in all_urls[::-1]:
        number = int(number_s)
        if number <= latest_vm:
            continue
        try:
            download_vm(name, url, number_s)
        except:
            logging.warning('VM {} FAILED TO DOWNLOAD! URL: {} NUMBER: {}'.format(name, url, number_s))
        if number > largest_downloaded:
            largest_downloaded = number

    # Update the 'most recent' file
    with open(most_recent_file, 'w') as f:
        f.write(str(largest_downloaded))







if __name__ == '__main__':
    main()

