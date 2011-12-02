# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
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
"""BibFormat element - Prints texkey with string mods for harvmac
"""


def format_element(bfo, harvmac=False):
    #Print Tex key harvmac variable set to true in harvmac.bfo in format_templates.

#    key = ''
#    for external_keys in bfo.fields("035"):
#        if external_keys['9'] == "SPIRESTeX" and external_keys['z']:
#            key = external_keys['z']

    key = get_spires_texkey(bfo)
    if not key:
        key = get_generated_texkey(bfo)

#        #contruct key in spires like way  need to store an make unique
#        ####FIXME
#        key = bfo.field("100a").split(' ')[0].lower() + ":" + \
#              bfo.field("269c").split('-')[0] + \
#              chr((recID % 26) + 97) + chr(((recID / 26) % 26) + 97)

    if str(harvmac).upper() == "TRUE":
        key = texkey_to_harvmac(key)

#        #split the texkey brooks:2010zza to be brooksZZA
#        var1 = key.split(':')
#        for i in range(0,10):
#           var1[1] = var1[1].replace(str(i),'')
#        key = var1[0] + var1[1].upper()
    return key


def get_spires_texkey(bfo):
    """Return spires texkey, if one is set, or else empty string."""
    for keys in bfo.fields("035__"):
        try:
            if keys['9'] == "SPIRESTeX" and keys['z']:
                return keys['z']
        except KeyError:
            return ''


def get_generated_texkey(bfo):
    """Return a spires-like texkey generated on the fly from the record.

    This texkey is not actually stored on the record and will not be
    searchable.  It is also not guaranteed to be unique.  Nevertheless, it is
    often better than nothing.

    FIXME: For collaboration papers without a first author, should use
    collaboration name.
    """
    key = bfo.field("100a").split(' ')[0].lower() + ":" + \
          bfo.field("269c").split('-')[0] + \
          chr((recID % 26) + 97) + chr(((recID / 26) % 26) + 97)
    return key


def texkey_to_harvmac(texkey):
    """Harvmac has its own idiosyncratic way to generate and display texkeys

    This mangles a texkey to return one in harvmac style.
    E.g., brooks:2010xy becomes brooksXY
    Failures return the empty string.
    """
    namepart, yearext = texkey.split(':')
    yearext = filter(lambda c: not c.isdigit(), yearext)
    return namepart + yearext.upper()


# we know the argument is unused, thanks
# pylint: disable-msg=W0613
def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
# pylint: enable-msg=W0613
