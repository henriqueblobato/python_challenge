import controller.logit
import MySQLdb
import traceback
import netaddr
import service.geoip
import service.rdap
class IPEntry(controller.logit.Logit):
    CONST_IPLIST_TOTAL_SELECTOR = 1
    CONST_IPLIST_COUNT_SELECTOR = 2
    def __init__(self):
        super(IPEntry, self).__init__(__name__)

    def get_connection(self):
        return MySQLdb.connect(host="some-mysql", user="user",
                            passwd="78df46013", db="fbg")
    def get_ips(self):
        db = self.get_connection()
        try:
            cur = db.cursor()
            cur.execute("""
            SELECT * FROM iplist
            """)
        finally:
            self.cleanup(db)
        return cur.fetchall()

    def find_all_ips(self, where_string, data):
        return self._call_db(lambda conn, cursor: self._find_all_ips(conn, cursor, where_string, data))

    def _find_all_ips(self, conn, cur, where_string, data):
        select_ip = ("select ip, ipcount, rdap_name, rdap_org_name, lat,lng, city, region, regioncode, country, countrycode from iplist " + where_string)
        cur.execute(select_ip, data)
        ret = []
        for (ip, ipcount, rdap_name, rdap_org_name, lat, lng, city, region, regioncode, country, countrycode) in cur.fetchall():
            d = {}
            d['ip'] = str(netaddr.IPAddress(ip))
            d['ipcount'] = str(ipcount)
            d['rdap_name'] = rdap_name
            d['rdap_org_name'] = rdap_org_name
            d['lat'] = str(lat)
            d['lng'] = str(lng)
            d['city'] = city
            d['region'] = region
            d['regioncode'] = regioncode
            d['country'] = country
            d['countrycode'] = countrycode
            ret.append(d)
        return ret

    def get_iplist_total(self):
        return self._call_db(lambda conn, cursor: self._get_iplist_total(conn, cursor))

    def _get_iplist_total(self, conn, cur):
        select = ("select count(*) from iplist")
        cur.execute(select)
        total = cur.fetchone()
        return total[0]

    def get_appstat_total(self, key):
        return self._call_db(lambda conn, cursor: self._get_appstat_total(conn, cursor, key))

    def _get_appstat_total(self, conn, cur, key):
        select = ("select total from appstat where id = %s")
        data = (key,)
        cur.execute(select, data)
        total = cur.fetchone()
        return total[0]

    def update_total(self,key, total):
        return self._call_db(lambda conn, cursor: self._update_total(conn, cursor,key, total))

    def _update_total(self, conn, cur,key, total):
        try:
            appstat_ins = ("REPLACE INTO appstat (id, total) values (%s, %s)")
            data = (key, total,)
            cur.execute(appstat_ins, data)
            conn.commit()
        except Exception, e:
            self.logger.error(str(e))

    def _call_db(self, f):
        db = self.get_connection()
        db.set_character_set('utf8')
        self.info('Got connection')
        try:
            cur = db.cursor()
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            # float(geoip_dict['latitude']), float(geoip_dict['longitude']),
            return f(db, cur)
        except Exception, e:
            self.logger.error(str(e))
            traceback.print_exc()
        finally:
            cur.close()
            self.cleanup(db)

    def add_ip(self, ips):
        self._call_db(lambda conn, cursor: self._add_ip(conn, cursor, ips))

    def _add_ip(self, conn, cur, ips):
        self.update_total(IPEntry.CONST_IPLIST_COUNT_SELECTOR, 0)
        create_ip = ("INSERT INTO iplist (ip, ipcount, rdap_name, rdap_org_name, lat,lng, city, region, regioncode, country, countrycode) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        geoip = service.geoip.GeoIP()
        rdap = service.rdap.RDAP()
        count = 0
        for ip in ips:
            try:
                self.info("Processing ip " + ip)
                geoip_dict = geoip.get_geo_ip(ip)

                try:
                    rdap.load_rdap(ip)
                except Exception, e:
                    self.logger.error(str(e))

                # self.info(geoip_dict['city'])
                data_ip = (int(netaddr.IPAddress(ip)), ips[ip], rdap.get_name(), rdap.get_org_name(), float(geoip_dict['latitude']), float(geoip_dict['longitude']),geoip_dict['city'],geoip_dict['region_name'], geoip_dict['region_code'], geoip_dict['country_name'], geoip_dict['country_code'],)
                cur.execute(create_ip, data_ip)
                conn.commit()
                count += 1
                self.update_total(IPEntry.CONST_IPLIST_COUNT_SELECTOR, count)
            except Exception, e:
                self.logger.error(str(e))
                traceback.print_exc()

    def cleanup(self, db):
        db.close()