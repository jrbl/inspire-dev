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

# pylint: disable=C0103
"""INSPIRE HEP Project Web Interface URL Handlers"""

import invenio.template
from invenio.bibtask import task_low_level_submission
from invenio.config import CFG_SITE_URL
from invenio.urlutils import redirect_to_url
from invenio.webinterface_handler import WebInterfaceDirectory
from invenio.bibtask import write_message


navtrail = (' <a class="navtrail" href=\"%s/inspire\">INSPIRE Utilities</a> '
            ) % CFG_SITE_URL


class WebInterfaceInspirePages(WebInterfaceDirectory):
    """Defines the set of /inspire pages."""

    _exports = ['', '/', 'file_upload']

    def __init__(self, recid=None):
        self.recid = recid
        self.template = invenio.template.load('inspireproject')

    def index(self, request):
        redirect_to_url(request, '%s' % CFG_SITE_URL)

    def file_upload(self, request, form):
        """Accept a stream of bytes for the disk and some metadata for the DB"""

        # form elements: username, recid, etc.  Layout is *like* cgi.FieldStorage, which is sorta like a dict.
        recid =        form.get('recid',       None).value
        bytes =        form.get('filedata',    None).value
        bytes_path =   form.get('filename',    None).value
        user_email =   form.get('username',    None).value
        user_name =    form.get('realname',    None).value
        user_comment = form.get('usercomment', None).value

        if recid and bytes and bytes_path and user_email:
            fext = '.'+bytes_path.split('.').pop()
            fpath = self._write_temporary_file(bytes, 'inspire_file_upload', fext)
            marcbytes = self._get_bibupload_marc_snippet(recid, fpath)
            mpath = self._write_temporary_file(marcbytes, 'inspire_upload_fft', '.marcxml')
            task_low_level_submission('bibupload', 'file_upload', '-P', '5', '-c', '%s' % mpath)
            self._write_ticket(recid, fpath, user_email, user_name, user_comment)
            return invenio.webpage.page(title = "File Upload OK",
                                        body = 'The file upload seems to have gone fine.  It has gone to a human reviewer and should appear online in a few days.',
                                        req = request)
        return invenio.webpage.page(title = "File Upload Error", body = "There were one or more unrecoverable errors during upload processing.  Please try again.", req=request)

    def __call__(self, req, form):
        """Redirect calls without final slash."""
        redirect_to_url(req, '%s/inspire/' % (CFG_SITE_URL))

    def _write_temporary_file(self,bytes, pre='file_upload', suf=''):
        """Write bytes to a secure temporary file.  Return its path."""
        import tempfile, os
        fd, fpath = tempfile.mkstemp(prefix=pre, suffix=suf)
        os.write(fd, bytes)
        os.close(fd)
        return fpath

    def _write_ticket(self, recid, fpath, user_email, user_name, user_comment):
        from invenio import bibcatalog
        ticketer = bibcatalog.BibCatalogSystemRT()

        url = CFG_SITE_URL + "/submit/managedocfiles?recid=" + recid
        ticket_content = "New Thesis:\n\n%s\n\nsubmitted by:\n\n%s\n\nuser comments:\n%s\n\nfile is at:\n%s\n in case of problems." % (url,user_email, user_comment,fpath)

        ticket_id = ticketer.ticket_submit(subject = 'New File Submitted!',
                              recordid = recid,
                              requestor = user_email,
                              queue = 'Test',
                              owner = 'tcb')

        if ticketer.ticket_comment(None, ticket_id, ticket_content) == None:
            write_message("Error: commenting on ticket %s failed." % (str(ticket_id),))
        return ticket_id

    def _get_bibupload_marc_snippet(self, recid, fullpath):
        return """<record>
       <controlfield tag="001">%(recid)s</controlfield>
       <datafield tag="FFT" ind1=" " ind2=" ">
           <subfield code="a">%(fullpath)s</subfield>
           <subfield code="n">%(nameto)s</subfield>
           <subfield code="t">INSPIRE-PUBLIC</subfield>
           <subfield code="r">restricted</subfield>
       </datafield>
   </record>""" % {'recid': recid,
                   'fullpath': fullpath,
                   'nameto': 'thesis'+recid,
                  }

