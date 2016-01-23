# -*- coding: utf-8 -*-
from datetime import datetime
import urllib2
import base64
import hmac, hashlib

from config import loadconf


class AmazonProdAdvertisingAPI(object):
    """
    Wrapper for Amazon Product Advertising APIs.

    Currently supports the following operations only:
        * Search Items

    参考：
        http://docs.aws.amazon.com/AWSECommerceService/latest/DG/ItemSearch.html
        http://www.ajaxtower.jp/ecs/para/index11.html
        http://blog.mudaimemo.com/2009/05/amazon-product-advertising-apipython.html
        https://bitbucket.org/basti/python-amazon-product-api/src/41529579819c75ff4f03bc93ea4f35137716ebf2/amazonproduct/api.py?at=default&fileviewer=file-view-default#cl-143

        リクエストパラメタ一覧：
        http://docs.aws.amazon.com/AWSECommerceService/latest/DG/CommonRequestParameters.html
    """
    def __init__(self, access_key_id, secret_key, associate_tag):
        self.access_key_id = access_key_id
        self.secret_key = secret_key
        self.associate_tag = associate_tag

        self.uri = 'webservices.amazon.co.jp'
        self.end_point = '/onca/xml'

    def item_lookup(self, keyword, searchIndex):
        options = dict()
        options['Operation'] = 'ItemSearch'
        options['Keywords'] = keyword
        options['SearchIndex'] = searchIndex or None

        """
        Response Groups
        http://docs.aws.amazon.com/ja_jp/AWSECommerceService/latest/DG/CHAP_ResponseGroupsList.html
        """
        response_groups = [
            'Images',
            'ItemIds',
            'Medium',
        ]
        options['ResponseGroup'] = ','.join(response_groups)

        return self._generate_url(options)

    def _generate_timestamp(self):
        # TODO: Need to convert GMT
        now = datetime.now()
        return now.strftime('%Y-%m-%dT%H:%M:%SZ')

    def _generate_url(self, options):
        options['Service'] = 'AWSECommerceService'
        options['AWSAccessKeyId'] = self.access_key_id
        options['AssociateTag'] = self.associate_tag
        options['Timestamp'] = self._generate_timestamp()

        # 'None' が含まれている場合は削除する.
        for k, v in options.items():
            if v is None:
                del options[k]

        # 署名(v2)を作成する.
        keys = sorted(options.keys())
        args = '&'.join('%s=%s' % (key, urllib2.quote(unicode(options[key])
                        .encode('utf-8'), safe='~')) for key in keys)

        msg = 'GET'
        msg += '\n' + self.uri
        msg += '\n' + self.end_point
        msg += '\n' + args

        hmac.new(self.secret_key or '', msg, hashlib.sha256).digest()
        signature = urllib2.quote(
            base64.b64encode(hmac.new(self.secret_key or '', msg, hashlib.sha256).digest()))

        url = "http://%s%s?%s&Signature=%s" % (self.uri, self.end_point, args, signature)

        return url


def main():
    config = loadconf()
    aaa = AmazonProdAdvertisingAPI(**config)

    """
    Search Index (JP)
    http://docs.aws.amazon.com/ja_jp/AWSECommerceService/latest/DG/LocaleJP.html
    """
    # print aaa.item_lookup(u'翔泳社', searchIndex="Books")
    print aaa.item_lookup(u'デジタルカメラ', searchIndex="Electronics")

if __name__ == "__main__":
    main()
