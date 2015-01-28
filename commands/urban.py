# Copyright (C) 2013-2014 Fox Wilson, Peter Foley, Srijay Kasturi, Samuel Damashek, James Forcier and Reed Koser
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from simplejson import JSONDecodeError
from urllib.parse import unquote
from requests import get
from requests.exceptions import ReadTimeout
from helpers.command import Command


def get_random():
    url = get('http://www.urbandictionary.com/random.php').url
    url = url.split('=')[1].replace('+', ' ')
    return unquote(url)


def get_definition(msg):
    msg = msg.split()
    index = msg[0][1:] if msg[0].startswith('#') else None
    term = " ".join(msg[1:]) if index is not None else " ".join(msg)
    try:
        req = get('http://api.urbandictionary.com/v0/define', params={'term': term}, timeout=10)
        data = req.json()['list']
    except JSONDecodeError:
        return "UrbanDictionary is having problems."
    except ReadTimeout:
        return "UrbanDictionary timed out."
    if len(data) == 0:
        output = "UrbanDictionary doesn't have an answer for you."
    elif index is None:
        output = data[0]['definition']
    elif not index.isdigit() or int(index) > len(data) or int(index) == 0:
        output = "Invalid Index"
    else:
        output = data[int(index)-1]['definition']
    output = output.splitlines()
    return ' '.join(output)


@Command('urban')
def cmd(send, msg, args):
    """Gets a definition from urban dictionary.
    Syntax: !urban (#<num>) <term>
    """
    if msg:
        output = get_definition(msg)
    else:
        msg = get_random()
        output = "%s: %s" % (msg, get_definition(msg))
    if len(output) > 256:
        output = output[:253] + "..."
    send(output)
