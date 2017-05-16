import re
import logit
import service.ipentry

class Parser(logit.Logit):

    def __init__(self):
        super(Parser, self).__init__(__name__)

    def add_num(self, a, b):
        return a+b

    def find_ips(self, file_name):
        """
        return dictionary of ip addresses to count
        :param file_name:
        :return:
        """
        ip_to_count = {}
        with open(file_name) as f:
            line = f.read()
            self.info(line)
            ips = self.get_all_ips(line)
            self.info("List IPs")
            for ip in ips:
                self.info(ip)
                if ip_to_count.has_key(ip):
                    ip_to_count[ip] += 1
                else:
                    ip_to_count[ip] = 1

        return ip_to_count
    def persist_ips(self, ip_dict):
        ipentry = service.ipentry.IPEntry()
        ipentry.update_total(service.ipentry.IPEntry.CONST_IPLIST_TOTAL_SELECTOR,len(ip_dict))
        ipentry.add_ip(ip_dict)

    def get_all_ips(self, line):
        return re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
