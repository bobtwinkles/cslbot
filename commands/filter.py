# Copyright (C) 2013 Fox Wilson, Peter Foley, Srijay Kasturi, Samuel Damashek, James Forcier and Reed Koser
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

from helpers.command import Command
from helpers.textutils import gen_fwilson, gen_creffett, gen_slogan, gen_insult, gen_morse


@Command('filter', ['handler', 'is_admin', 'nick'])
def cmd(send, msg, args):
    """Changes the output filter.
    Syntax: !filter <filter|list|reset>
    """
    output_filters = {
        "fwilson": gen_fwilson,
        "creffett": gen_creffett,
        "slogan": gen_slogan,
        "insult": gen_insult,
        "morse": gen_morse
        }
    if not msg:
        names = []
        for i in args['handler'].outputfilter:
            name = i.__name__
            if name == '<lambda>':
                name = 'passthrough'
            else:
                name = name[4:]
            names.append(i)
        send("Current filter(s): %s" % ", ".join(names))
    elif msg == 'list':
        send("Available filters are %s" % ", ".join(output_filters.keys()))
    elif msg == 'reset' or msg == 'passthrough':
        if args['is_admin'](args['nick']):
            args['handler'].outputfilter = [lambda x: x]
            send("Okay!")
        else:
            send("Nope, not gonna do it!")
    elif msg.startswith('chain'):
        next_filter = msg.split()[1]
        if next_filter in output_filters.keys():
            args['handler'].outputfilter.append(output_filters[next_filter])
            send("Okay!")
        else:
            send("Nope, not gonna do it.")
    elif msg in output_filters.keys():
        if args['is_admin'](args['nick']):
            args['handler'].outputfilter = [output_filters[msg]]
            send("Okay!")
        else:
            send("Nope, not gonna do it!")
    else:
        send("Invalid filter.")
