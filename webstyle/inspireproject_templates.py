import invenio.config


class Template:
    """Tell Invenio how to produce output for our various URLs"""

    def __init__(self):
        """Establish some variables we can use throughout"""
        self.site_url = invenio.config.CFG_SITE_URL
        self.javascript = [ # prerequisites for hotkeys, autocomplete
                           'jquery-1.4.4.js',
                           'jquery-ui.min.js',
                          ]

    def setup_scripts(self):
        """Output a bunch of <script> bits."""
        ostr = ''
        for script in self.javascript:
            if script.startswith('http'):
                ostr += ("<script type=\"text/javascript\" src=\"%s\">" % script)
            else:
                ostr += ("<script type=\"text/javascript\" src=\"%s/js/%s\">" %
                                           (invenio.config.CFG_SITE_URL, script))
            ostr += "</script>\n"
        return ostr

    def index(self):
        o = self.setup_scripts()
        o += "<form method=\"post\" action=\"%s\"><input type=\"file\" name=\"filedata\" /></form>" % (self.site_url + '/inspire/thesis_upload')
        o += "<input id=\"submit_button\" name=\"submit_button\" type=\"submit\" value=\"Submit\" class=\"formbutton\" />"
        return o

    def tPara(self, instr, indent=0, tagas=''):
        """Output an HTML paragraph"""
        ostr  = ' '*indent + "<p id=%s>\n" % tagas
        ostr += ' '*indent + "%s\n" % instr
        ostr += ' '*indent + '</p>\n'
        return ostr

    def tList(self, lst, indent=0, tagas=''):
        """Output an HTML list"""
        ostr = ' '*indent + "<ul class=\"%s\">\n" % tagas
        for item in lst:
            ostr += ' '*indent + " <li>%s</li>\n" % str(item)
        ostr += ' '*indent + '</ul>\n'
        return ostr
