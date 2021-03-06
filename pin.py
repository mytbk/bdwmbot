from bs4 import BeautifulSoup
import requests
import json
import sys
from functools import reduce
from board_list import all_boards
from util import tag_to_str
import copy

bdwm_url = 'https://bbs.pku.edu.cn/v2/'


def find_pins(html):
    return list(map(lambda x: x.parent.parent, html.find_all('div', class_='pin')))


def pin_html_to_item(html):
    url = bdwm_url + html.a['href']
    tdiv = html.find('div', class_='title')
    title = tdiv.contents[0]
    return {'url': url, 'title': title}


def get_pins(id):
    board_url = 'https://bbs.pku.edu.cn/v2/thread.php?bid={}'.format(id)
    for i in range(0, 3):
        try:
            r = requests.get(board_url, timeout=2**i)
            break
        except:
            sys.stderr.write(
                '[board {}] Request error #{}\n'.format(id, i))
            r = None

    if r is None:
        return None

    soup = BeautifulSoup(r.content, 'html.parser')
    pins = find_pins(soup)
    return list(map(pin_html_to_item, pins))


def board2id(board):
    bid = all_boards.get(board, -1)
    if bid == -1:
        bnames = all_boards.keys()
        for b in bnames:
            if b.lower() == board.lower():
                return all_boards[b]
        return -1
    else:
        return bid


# maybe we don't need this...
def get_boardid(board):
    headers = requests.utils.default_headers()
    headers.update({'Referer': 'https://bbs.pku.edu.cn/v2/home.php'})
    r = requests.post('https://bbs.pku.edu.cn/v2/ajax/get_topsearch.php',
                      {'pref': board}, headers=headers)
    j = json.loads(r.content)
    return j['boards'][0]['id']


def read_post(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tgt = soup.find('div', class_='body')

    for aa in tgt.find_all('a'):
        href = aa['href'].replace('jump-to.php?url=', '').replace('%2F', '/').replace('%3A', ':')
        aa['href'] = href
        del aa['data-no-pjax']
        del aa['style']
        del aa['target']

    tgt2 = BeautifulSoup('', 'html.parser')
    isText = False
    tmps = ''
    for i in tgt.contents:
        if i.find('br') is not None:
            isText = True

        if isText:
            if i.string is not None:
                tmps = tmps + str(i.string)
            else:
                if len(tmps) > 0:
                    _s = BeautifulSoup('<p>' + tmps + '</p>', 'html.parser')
                    tgt2.append(_s)
                    tmps = ''
                tgt2.append(copy.copy(i))
        else:
            tgt2.append(copy.copy(i))

    html = str(tgt2)
    txt = reduce(lambda x, y: x + '\n' + y,
                 map(lambda t: tag_to_str(t), tgt2.contents))

    return txt, html
