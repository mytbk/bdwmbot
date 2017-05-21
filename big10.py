#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests

bdwm_url = 'https://bbs.pku.edu.cn/v2/'


def make_item(div):
    url = bdwm_url + div.a['href']
    tdiv = div.find('div', class_='title')
    title = tdiv.contents[0]
    return {'url': url, 'title': title}


def get_hottopic(num):
    r = requests.request(
        method='get', url='https://bbs.pku.edu.cn/v2/hot-topic.php')
    soup = BeautifulSoup(r.content, 'html.parser')
    topics = soup.find_all('div', class_='list-item-topic')
    if num > 100:
        num = 100
    top_topics = topics[0:num]
    return list(map(make_item, top_topics))


def link_dict(a_link):
    return {'url': bdwm_url + a_link['href'], 'title': a_link.contents[0]}


def get_big10():
    r = requests.request(
        method='get', url='https://bbs.pku.edu.cn/v2/home.php')
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        big10 = soup.find_all('section', class_='big-ten')[0]
    except:
        return None

    big10_links = big10.find_all('a', class_='post-link')
    return list(map(link_dict, big10_links))
