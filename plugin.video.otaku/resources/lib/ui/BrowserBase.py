# -*- coding: utf-8 -*-
import base64

import six
from resources.lib.ui import client
from six.moves import urllib_parse


class BrowserBase(object):
    _BASE_URL = None

    def _clean_title(self, text):
        return text.replace(u'×'.encode('utf-8') if six.PY2 else u'×', ' x ')

    def _to_url(self, url=''):
        assert self._BASE_URL is not None, "Must be set on inherentance"

        if url.startswith("/"):
            url = url[1:]
        return "%s/%s" % (self._BASE_URL, url)

    def _send_request(self, url, data=None, headers=None, XHR=False):
        return client.request(url, post=data, headers=headers, XHR=XHR)

    def _post_request(self, url, data={}, headers=None):
        return self._send_request(url, data, headers)

    def _get_request(self, url, data=None, headers=None, XHR=False):
        if data:
            url = "%s?%s" % (url, urllib_parse.urlencode(data))
        return self._send_request(url, data=None, headers=headers, XHR=XHR)

    def _get_redirect_url(self, url, headers=None):
        t = client.request(url, redirect=False, headers=headers, output='extended')
        if t:
            return t[2].get('Location')
        return ''

    def _bencode(self, text):
        return six.ensure_str(base64.b64encode(six.ensure_binary(text)))

    def _bdecode(self, text):
        return six.ensure_str(base64.b64decode(text))

    def _get_origin(self, url):
        purl = urllib_parse.urlparse(url)
        return '{0}://{1}'.format(purl.scheme, purl.netloc)

    def _get_size(self, size=0):
        power = 1024.0
        n = 0
        power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB'}
        while size > power:
            size /= power
            n += 1
        return '{0:.2f} {1}'.format(size, power_labels[n])
