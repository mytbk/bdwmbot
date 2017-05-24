#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import sys
import io

bdwm_url = 'https://bbs.pku.edu.cn/v2/'


def get_boardname(id):
    board_url = 'https://bbs.pku.edu.cn/v2/thread.php?bid={}'.format(id)
    for i in range(0, 10):
        try:
            r = requests.get(board_url, timeout=2**i)
            break
        except requests.exceptions.Timeout:
            sys.stderr.write('[board {}] Timeout for request #{}\n'.format(id, i))

    soup = BeautifulSoup(r.content, 'html.parser')
    bnspan = soup.find('span', class_='eng')
    if bnspan is None:
        return None
    else:
        return bnspan.contents[0]


f = io.open('board_list.py', mode='w')
f.write('all_boards = {\n')
for i in range(1,1096):
    bn = get_boardname(i)
    if bn is not None:
        f.write('    \'{}\': {},\n'.format(bn, i))
f.write('}\n')
f.close()
