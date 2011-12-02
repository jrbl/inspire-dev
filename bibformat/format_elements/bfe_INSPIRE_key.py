# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Get a key for this item, hopefully unique.

Try to get the SPIRES TexKey from 035z, then if that's missing, return the
arxiv ID (eprint #).  IF that's not there, then try report number, and 
barring that return the INSPIRE recid for the record.

Cf. bfe_INSPIRE_bibtex for a different way to failover when no 035z is found.
"""


from invenio.bibformat_elements import bfe_report_numbers as bfe_repno
from invenio.bibformat_elements import bfe_texkey
from invenio.bibformat_elements.bfe_INSPIRE_arxiv import get_arxiv

#    key = ''
#    for external_keys in bfo.fields("035"):
#        if external_keys['9'] == "SPIRESTeX" and external_keys['z']:
#            key = external_keys['z']
#    if not key:
#        #contruct key in spires like way  need to store an make unique
#        ####FIXME
#        key = bfo.field("100a").split(' ')[0].lower() + ":" + \
#              bfo.field("269c").split('-')[0] + \
#              chr((recID % 26) + 97) + chr(((recID / 26) % 26) + 97)
#    out += key + ','
#
#        #If author cannot be found, print a field key=recID
#    import invenio.bibformat_elements.bfe_INSPIRE_authors as bfe_authors
#    authors = bfe_authors.format_element(bfo=bfo,
#                                 limit="5",
#                                 separator=" and ",
#                                 extension=" and others",
#                                 collaboration = "no",
#                                 print_links="no",
#                                 name_last_first = "yes")
#    if authors:
#        out += texified("author", authors)
#    else:
#        out += texified("key", recID)


def format_element(bfo):
    return get_key_formatted(bfo)


def get_key_formatted(bfo):

    # Try to get the SPIRES TexKey if one is stored on the record
    out = bfe_texkey.get_spires_texkey(bfo)

    # Failing that, return arxiv ID if its available
    if not out:
        out = get_arxiv(bfo, category="no")
        if out:
            out = out[0]

    # No arxiv id?  How about a report number?
    if not out:
        out = bfe_repno.get_report_numbers_formatted(bfo, '', '1', extension='')

    # Fail to constructing a texkey.  See caveats in its docstring:
    if not out:
        out = bfe_texkey.get_generated_texkey(bfo)
        
    # No arxiv id and no report number.  Fail to recid
    if not out:
        return bfo.recID

    # Somewhere up above we got something useful; return it
    return out


# we know the argument is unused, thanks
# pylint: disable-msg=W0613
def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
# pylint: enable-msg=W0613
