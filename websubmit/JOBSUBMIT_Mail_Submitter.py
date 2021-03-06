## This file is part of Invenio.
## Copyright (C) 2004, 2005, 2006, 2007, 2008, 2010, 2011 CERN.
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

__revision__ = "$Id$"

   ##
   ## Name:          JOBSUBMIT_Mail_Submitter.py
   ## Description:   function JOBSUBMIT_Mail_Submitter
   ##                This function sends a confirmation email to the submitter
   ##             of the document
   ## Author:         T.Baron
   ##
   ## PARAMETERS:    authorfile: name of the file containing the author
   ##             titleFile: name of the file containing the title
   ##             emailFile: name of the file containing the email
   ##             status: one of "ADDED" (the document has been integrated
   ##                     into the database) or "APPROVAL" (an email has
   ##                 been sent to a referee - simple approval)
   ##             edsrn: name of the file containing the reference
   ##             newrnin: name of the file containing the 2nd reference
   ##                     (if any)
   ## OUTPUT: HTML
   ##

import os
import re

from invenio.config import CFG_SITE_NAME, \
     CFG_SITE_URL, \
     CFG_SITE_SUPPORT_EMAIL, \
     CFG_SITE_RECORD, \
     CFG_SITE_LANG, \
     CFG_SITE_NAME_INTL

from invenio.websubmit_config import CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN
from invenio.mailutils import send_email
from invenio.messages import wash_language, gettext_set_language

CFG_WEBSUBMIT_JOBS_SUPPORT_EMAIL = "jobs@inspirehep.net"
CFG_WEBSUBMIT_JOBS_FROMADDR = 'INSPIRE-HEP Jobs support <%s>' % (CFG_WEBSUBMIT_JOBS_SUPPORT_EMAIL,)

def JOBSUBMIT_Mail_Submitter(parameters, curdir, form, user_info=None):
    """
    This function send an email to the submitter to warn him the
    document he has just submitted has been correctly received.

    Parameters:

      * authorfile: Name of the file containing the authors of the
                    document

      * titleFile: Name of the file containing the title of the
                   document

      * emailFile: Name of the file containing the email of the
                   submitter of the document

      * status: Depending on the value of this parameter, the function
                adds an additional text to the email.  This parameter
                can be one of: ADDED: The file has been integrated in
                the database.  APPROVAL: The file has been sent for
                approval to a referee.  or can stay empty.

      * edsrn: Name of the file containing the reference of the
               document

      * newrnin: Name of the file containing the 2nd reference of the
                 document (if any)
    """
    # retrieve report number
    edsrn = parameters['edsrn']
    newrnin = parameters['newrnin']
    fp = open("%s/%s" % (curdir,edsrn),"r")
    rn = fp.read()
    fp.close()
    rn = re.sub("[\n\r]+","",rn)
    if newrnin != "" and os.path.exists("%s/%s" % (curdir,newrnin)):
        fp = open("%s/%s" % (curdir,newrnin),"r")
        additional_rn = fp.read()
        fp.close()
        additional_rn = re.sub("[\n\r]+","",additional_rn)
        fullrn = "%s and %s" % (additional_rn,rn)
    else:
        fullrn = rn
    fullrn = fullrn.replace("\n"," ")
    # The title is read from the file specified by 'titlefile'
    try:
        fp = open("%s/%s" % (curdir,parameters['titleFile']),"r")
        m_title = fp.read().replace("\n"," ")
        fp.close()
    except:
        m_title = "-"
    # The name of the author is read from the file specified by 'authorfile'
    try:
        fp = open("%s/%s" % (curdir,parameters['authorfile']),"r")
        m_author = fp.read().replace("\n"," ")
        fp.close()
    except:
        m_author = "-"
    # The submitters email address is read from the file specified by 'emailFile'
    try:
        fp = open("%s/%s" % (curdir,parameters['emailFile']),"r")
        m_recipient = fp.read().replace ("\n"," ")
        fp.close()
    except:
        m_recipient = ""
    # create email body
    email_txt = "The job listing with reference number %s\nTitle: %s\nSubmitter(s): %s\n\nhas been received for approval.\n\n" % (fullrn,m_title,m_author)
    # The user is either informed that the document has been added to the database, or sent for approval
    email_txt += "Your listing will not be visible until it has been fully approved by one of our catalogers. " \
                 "When this happens, you will be warned by email.\n\n" \
                 "If you detect an error, please let us know by sending an email to %s. \n\n" \
                 "Thank you for using the HEP Jobs submission.\n" % (CFG_WEBSUBMIT_JOBS_SUPPORT_EMAIL,)
    # send the mail
    send_email(fromaddr=CFG_WEBSUBMIT_JOBS_FROMADDR, toaddr=m_recipient.strip(), subject="%s: Document Received" % fullrn, \
               content=email_txt, footer=job_email_footer(), copy_to_admin=CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN)
    return ""

def job_email_footer(ln=CFG_SITE_LANG):
    """The footer of the email from JobSubmit
    @param ln: language
    @return: footer as a string"""
    ln = wash_language(ln)
    _ = gettext_set_language(ln)
    #standard footer
    out = """\n\n%(best_regards)s
--
%(sitename)s <%(siteurl)s>
%(need_intervention_please_contact)s <%(sitesupportemail)s>
        """ % {
            'sitename': CFG_SITE_NAME_INTL[ln],
            'best_regards': _("Best regards"),
            'siteurl': CFG_SITE_URL,
            'need_intervention_please_contact': _("Need human intervention?  Contact"),
            'sitesupportemail': CFG_WEBSUBMIT_JOBS_SUPPORT_EMAIL
            }
    return out

