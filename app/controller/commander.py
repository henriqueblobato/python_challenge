# -*- coding: utf-8 -*-
import parser
import filter
import service.ipentry
import service.geoip
import service.rdap
import logging
import pprint

import logit
class Commander(logit.Logit):
    total = 0
    def __init__(self):
        super(Commander, self).__init__(__name__)

    def rdap_test(self, ip):
        rdap = service.rdap.RDAP()
        rdap.load_rdap(ip)
        print rdap.get_name()
        print rdap.get_org_name()


    def reset(self,key, val):
        ipentry = service.ipentry.IPEntry()
        ipentry.update_total(key, val)

    def get_parse_status(self):
        ipentry = service.ipentry.IPEntry()
        prog = ipentry.get_appstat_total(service.ipentry.IPEntry.CONST_IPLIST_COUNT_SELECTOR)
        total = ipentry.get_appstat_total(service.ipentry.IPEntry.CONST_IPLIST_TOTAL_SELECTOR)
        if total == -1:
            status = "done"
        else:
            status = "" + str(prog) + "/" + str(total)
        return status

    def parse(self, filename):
        p = parser.Parser()
        ip_dict = p.find_ips(filename)
        p.persist_ips(ip_dict)

    def run(self, query):
        p = parser.Parser()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # ip_dict = p.find_ips(filename)
        # p.persist_ips(ip_dict)
        self.info(query)
        f = filter.Filter()
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(f.get_ip(527279671))
        # o = f.parse_dsl(r'"ip" > "89.168.179.90"')
        o = f.parse_dsl(query)
        self.info(o)
        if 'error' in o:
            return o['error']
        else:
            r = f.get_results(o['where_string'], o['values'])
        self.info(r)
        return r


