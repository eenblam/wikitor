import json
import StringIO

import pycurl

from url import *

class WikiProxy(object):
    def __init__(self, url, socks_port, headers=None, connection_timeout=30):
        self.url = url
        self.headers = headers
        self.socks_port = socks_port
        self.connection_timeout = connection_timeout

    def _request(self, params):
        url = uri(self.url, params)
        output = StringIO.StringIO()

        query = pycurl.Curl()
        query.setopt(pycurl.URL, url)
        query.setopt(pycurl.PROXY, 'localhost')
        query.setopt(pycurl.PROXYPORT, self.socks_port)
        query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
        query.setopt(pycurl.CONNECTTIMEOUT, self.connection_timeout)
        query.setopt(pycurl.WRITEFUNCTION, output.write)

        try:
            # Probably want to:
            # Perform query
            # Push to database if good
            # If blocked, push back onto stack and reset tor
            query.perform()
            return output.getvalue()
        except pycurl.error as err:
            raise ValueError("Unable to reach %s (%s)"
                    .format(url, exc))

    def get(self, params):
        r = self._request(params)
        return r

    def get_json(self, params):
        r = self.get(params)
        try:
            js = json.loads(r)
        except ValueError:
            js = None
        return js

    def titles_from_query(self, query):
        params = {
            'format': 'json',
            'action': 'query',
            'list': 'search',
            'srwhat': 'text',
            'srsearch': query.strip()
        }
        res = self.get_json(params)
        #TODO Handle bad response
        return [x['title'] for x in res['query']['search']]

    def title_string_from_query(self, query):
        titles = self.titles_from_query(query)
        return '|'.join(titles)

    def titles_to_pageids(self, title_string):
        """Get pageids from title string"""
        params = {
            'format': 'json',
            'action': 'query',
            'titles': title_string
        }
        res = self.get_json(params)
        for pageid in get_query_keys(res):
            yield pageid

    def get_page_by_id(self, pageid):
        params = {
            'format': 'json',
            'action': 'parse',
            'prop': 'text',
            'pageid': pageid
        }
        res = self.get_json(params)
        try:
            page = res['parse']
        except TypeError:
            page = None
        return page

    def _get_content(self, title_string):
        result_stream = ((pageid, self.get_page_by_id(pageid))
                        for pageid
                        in self.titles_to_pageids(title_string))
        return ((pageid, get_title(x), get_text(x))
                for pageid,x in result_stream)
        #return ((pageid, x['title'], x['text']['*'])
        #        for pageid,x in result_stream)

    def gen_from_query(self, query):
        titles = self.title_string_from_query(query)
        data_stream = self._get_content(titles)
        return data_stream

def get_title(x):
    try:
        return x['title']
    except TypeError:
        return None

def get_text(x):
    try:
        return x['text']['*']
    except TypeError:
        return None

def get_query_keys(x):
    try:
        return x['query']['pages'].keys()
    except TypeError:
        return []
