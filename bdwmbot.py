"""
    bdwmbot: a bot using bdwm.net BBS
    Copyright (C) 2017  vimacs <vimacs.hacks@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler
import big10
from util import item_to_md_html
from pin import board2id, get_pins, read_post

# Global variables
USERNAME = ""  # Bot's username
PASSWORD = ""  # Bot's password
SERVER = ""  # Matrix server URL


def hottopic_callback(room, event):
    args = event['content']['body'].split()
    if len(args) == 1:
        print("Get big10 topics")
        topics = big10.get_big10()
        num = 10
    elif len(args) == 2:
        try:
            num = int(args[1])
            print("Get {} hottest topics".format(num))
            topics = big10.get_hottopic(num)
        except ValueError:
            room.send_text('usage: !hottopics [num]')
    else:
        room.send_text('usage: !hottopics [num]')

    print("Going to reply...")
    md, html = item_to_md_html(topics)
    room.send_html(html, body=md, msgtype="m.notice")


def pins_callback(room, event):
    args = event['content']['body'].split()
    if len(args) != 2:
        room.send_notice('usage: !pins <board name/id>')
        return

    try:
        bid = int(args[1])
    except ValueError:
        bid = board2id(args[1])

    if bid == -1:
        room.send_notice('Invalid board name/id!')
    pins = get_pins(bid)
    md, html = item_to_md_html(pins)
    room.send_html(html, body=md, msgtype="m.notice")


def lcpu_event_callback(room, event):
    def event_filter(e):
        kws = ['活动', '版聚', '通知']
        for i in kws:
            if i in e['title']:
                return True
        return False

    pins = get_pins(13)
    if pins is None:
        room.send_notice('Error getting pins of board Linux.')
        return
    events = list(filter(event_filter, pins))
    if len(events) == 0:
        room.send_notice('No events found.')
        return
    md, html = item_to_md_html(events)
    room.send_html(html, body=md, msgtype="m.notice")
    for e in events:
        txt, html = read_post(e['url'])
        room.send_html(html, body=txt, msgtype="m.notice")


def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    hottopic_handler = MCommandHandler("hottopics", hottopic_callback)
    bot.add_handler(hottopic_handler)

    pins_handler = MCommandHandler("pins", pins_callback)
    bot.add_handler(pins_handler)

    lcpu_event_handler = MCommandHandler("event", lcpu_event_callback)
    bot.add_handler(lcpu_event_handler)

    # Start polling
    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other
    # threads
    while True:
        input()


if __name__ == "__main__":
    main()
