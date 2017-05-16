import controller.logit
import requests
import traceback
import json
import StringIO
import xmltodict
import pprint
class RDAP(controller.logit.Logit):

    def __init__(self):
        super(RDAP, self).__init__(__name__)


    def load_rdap(self, ip):
        """
<?xml version='1.0'?>
<?xml-stylesheet type='text/xsl' href='http://whois.arin.net/xsl/website.xsl' ?>
    <net xmlns="http://www.arin.net/whoisrws/core/v1" xmlns:ns2="http://www.arin.net/whoisrws/rdns/v1" xmlns:ns3="http://www.arin.net/whoisrws/netref/v2"
        inaccuracyReportUrl="https://www.arin.net/public/whoisinaccuracy/index.xhtml" termsOfUse="https://www.arin.net/whois_tou.html">
        <registrationDate>2009-02-17T14:03:45-05:00</registrationDate>
        <ref>https://whois.arin.net/rest/net/NET-174-16-0-0-1</ref>
        <endAddress>174.31.255.255</endAddress>
        <handle>NET-174-16-0-0-1</handle>
        <name>QWEST-INET-127</name>
        <netBlocks>
            <netBlock>
                <cidrLength>12</cidrLength>
                <endAddress>174.31.255.255</endAddress>
                <description>Direct Allocation</description>
                <type>DA</type>
                <startAddress>174.16.0.0</startAddress>
            </netBlock>
        </netBlocks>
        <originASes>
            <originAS>AS209</originAS>
        </originASes>
        <resources inaccuracyReportUrl="https://www.arin.net/public/whoisinaccuracy/index.xhtml" termsOfUse="https://www.arin.net/whois_tou.html">
            <limitExceeded limit="256">false</limitExceeded>
        </resources>
        <orgRef handle="QCC-18" name="Qwest Communications Company, LLC">https://whois.arin.net/rest/org/QCC-18</orgRef>
        <parentNetRef handle="NET-174-0-0-0-0" name="NET174">https://whois.arin.net/rest/net/NET-174-0-0-0-0</parentNetRef>
        <startAddress>174.16.0.0</startAddress>
        <updateDate>2013-09-16T16:31:05-04:00</updateDate>
        <version>4</version>
    </net>
        :param ip:
        :return:
        """
        ret = {}
        url = 'http://whois.arin.net/rest/ip/'+ip
        response = requests.get(url)
        if response.ok:
            self.doc = xmltodict.parse(response.content)
        else:
            self.doc = None

    def get_name(self):
        self.name = ""
        if self.doc != None:
            try:
                self.name = self.doc['net']['name']  #['#text']
            except Exception, e:
                self.logger.error(str(e))
                self.logger.error(self.doc)
                traceback.print_exc()
        return self.name

    def get_org_name(self):
        self.org_name = ""
        if self.doc != None:
            try:
                self.org_name = self.doc['net']['orgRef']['@name']
            except Exception, e:
                self.logger.error(str(e))
                self.logger.error(self.doc)
                traceback.print_exc()
        return self.org_name
