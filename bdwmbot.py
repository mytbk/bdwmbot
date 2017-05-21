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
from functools import reduce
import big10

# Global variables
USERNAME = ""  # Bot's username
PASSWORD = ""  # Bot's password
SERVER = ""  # Matrix server URL


def hi_callback(room, event):
    # Somebody said hi, let's say Hi back
    room.send_text("Hi, " + event['sender'])


def echo_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)

    # Echo what they said back
    room.send_text(' '.join(args))

def hottopic_callback(room, event):
    args = event['content']['body'].split()
    if len(args) == 1:
        topics = big10.get_big10()
        num = 10
    elif len(args) == 2:
        try:
            num = int(args[1])
            topics = big10.get_hottopic(num)
        except ValueError:
            room.send_text('usage: !hottopics [num]')
    else:
        room.send_text('usage: !hottopics [num]')

    markdown_strs = list(map(lambda t: '[{}]({})'.format(t['title'], t['url']), topics))
    md = reduce(lambda s,t: s+'  \n'+t, markdown_strs)
    html_strs = list(map(lambda t: '<a href="{}">{}</a>'.format(t['url'], t['title']), topics))
    html = reduce(lambda s,t: s+'<br />\n'+t, html_strs)
    room.send_html(html, body=md, msgtype="m.notice")

def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    # Add a regex handler waiting for the word Hi
    #hi_handler = MRegexHandler("Hi", hi_callback)
    #bot.add_handler(hi_handler)

    hottopic_handler = MCommandHandler("hottopics", hottopic_callback)
    bot.add_handler(hottopic_handler)

    # Start polling
    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()


if __name__ == "__main__":
    main()
