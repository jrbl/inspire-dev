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
"""BibFormat element - INSPIRE Thesis Submission Form"""


from invenio.config import CFG_SITE_SUPPORT_EMAIL, CFG_SITE_URL


def format_element(bfo,onsubmit=""):
    """Create thesis submission form for record, after checking some variables.

    @param onsubmit: a js action to be taken onSubmit
    """

    recid = bfo.control_field("001")
    action = CFG_SITE_URL + "/inspire/file_upload"

    form = '''
<div id="thesis_upload_box" class="upload_box">
 <form name="fulltext_upload" method="post" onSubmit="%s" action="%s" enctype="multipart/form-data">
  <input type="hidden" name="recid" id="recid" value="%s" />
  <input type="hidden" name="filename" id="filename" value="" />

  <p class='big_text file_upload_note_p'>Share your thesis<br />
   <input type="file" class="big_text input_inherit_font" id="filedata" name="filedata" size="35" /><br />
   <span class="tiny_text">(Click Browse and select your thesis for upload.)</span>
  </p>
  <p class='big_text file_upload_note_p'><input class="prefill prefill_default_text big_text input_inherit_font prefill_box" name="username" id="username" prefill="Please enter your email address (mandatory)"/></p>
  <p class='file_upload_note_p'><input class="big_text prefill prefill_default_text input_inherit_font" size=35 name=realname id=realname prefill="Please enter your full name (optional)"/></p>
  <p class='file_upload_note_p'>
   <textarea class="prefill prefill_default_text input_inherit_font" name="usercomment" id=usercomment rows="2" cols=35 wrap=virtual prefill="...or any other data you think we should have (advisor, comments, etc.)">
   </textarea>
  </p>
  <p class='file_upload_note_p'>
   <input type="submit" name="submit" value="Upload My Thesis" class="formbutton formbutton_strong" />
  </p>

 </form>
</div>''' % (onsubmit,action,recid)

    if _is_thesis(bfo):
        return form
    else:
        return '''
<div class="note">
 <p id="thesis_upload_note">
  This paper does not appear to be a thesis, so submission is not available for this paper. If you believe this is
  an error, please contact us at <a href="mailto:%s">%s</a>
 </p>
</div>''' % (CFG_SITE_SUPPORT_EMAIL, CFG_SITE_SUPPORT_EMAIL)


# we know the argument is unused, thanks
# pylint: disable-msg=W0613
def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
# pylint: enable-msg=W0613

def _is_thesis(bfo):
    """Is bfo a thesis?"""
    for coll in bfo.fields("980__a"):
        if coll.lower() == "thesis":
            return True
    return False
