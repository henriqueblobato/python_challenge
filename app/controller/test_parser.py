import mock
import unittest
import logit
from netaddr import IPNetwork
from .parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):

        self.ipv4_addr_file_normal = """
54.169.236.254 - - [08/May/2017:07:01:00 -0400] "GET / HTTP/1.1" 200 5529 "-" "Mozilla/5.0 zgrab/0.x"
217.128.34.235 - - [08/May/2017:08:13:40 -0400] "GET / HTTP/1.1" 200 5529 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:49.0) Gecko/20100101 Firefox/49.0"
207.46.13.45 - - [08/May/2017:08:45:03 -0400] "GET / HTTP/1.1" 200 1337 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
89.248.168.117 - - [08/May/2017:08:46:34 -0400] "GET / HTTP/1.1" 200 12809 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
157.55.39.246 - - [08/May/2017:09:35:26 -0400] "GET / HTTP/1.1" 200 205 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
64.62.252.162 - - [08/May/2017:10:05:21 -0400] "GET /robots.txt HTTP/1.1" 404 136 "-" "BUbiNG (+http://180.76.15.33/BUbiNG.html)"
64.62.252.162 - - [08/May/2017:10:05:28 -0400] "GET /robots.txt HTTP/1.1" 404 136 "-" "BUbiNG (+http://law.di.unimi.it/BUbiNG.html)"
64.62.252.162 - - [08/May/2017:10:05:28 -0400] "GET / HTTP/1.1" 200 763 "-" "BUbiNG (+http://law.di.unimi.it/BUbiNG.html)"
64.62.252.162 - - [08/May/2017:10:05:35 -0400] "GET / HTTP/1.1" 200 2403 "-" "BUbiNG (+http://law.di.unimi.it/BUbiNG.html)"
23.247.72.34 - - [08/May/2017:10:23:05 -0400] "GET / HTTP/1.1" 200 12809 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)"
207.46.13.32 - - [08/May/2017:12:02:32 -0400] "GET / HTTP/1.1" 200 5529 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
180.76.15.135 - - [08/May/2017:12:12:54 -0400] "GET /robots.txt HTTP/1.1" 404 136 "-" "Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
180.76.15.5 - - [08/May/2017:12:12:54 -0400] "GET /robots.txt HTTP/1.1" 404 136 "-" "Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2"
180.76.15.12 - - [08/May/2017:12:13:08 -0400] "GET /connected_worlds/TemplateData/style.css HTTP/1.1" 200 1507 "-" "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
131.253.27.8 - - [08/May/2017:12:28:39 -0400] "GET /style/bullet.png HTTP/1.1" 200 989 "http://daretogame.net/" "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 BingPreview/1.0b"
207.46.13.32 - - [08/May/2017:12:28:40 -0400] "GET /robots.txt HTTP/1.1" 404 136 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
66.240.192.39 - - [08/May/2017:12:54:45 -0400] "\x00\x00\x00\x01" 400 166 "-" "-"
66.240.192.39 - - [08/May/2017:12:54:46 -0400] "PING" 400 166 "-" "-"
        """

    def test_ipnetwork(self):
        n = int(IPNetwork('8.8.8.8').ip)
        self.assertEquals(n, 134744072)
    def test_get_ipv4_address(self):
        with mock.patch('__builtin__.open', mock.mock_open(read_data=self.ipv4_addr_file_normal), create=True) as mocked:
            mocked.return_value.__iter__.return_value = self.ipv4_addr_file_normal.splitlines()
            parser = Parser()
            parser.info("Starting up")
            ip_dict = {}
            ip_dict = parser.find_ips("some_ip_file.txt")
            parser.info(ip_dict)
            self.assertEquals(len(ip_dict), 15)

