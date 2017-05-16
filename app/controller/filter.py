import service.ipentry
import logit
import parsley
import pprint
import netaddr
class Filter(logit.Logit):
    def __init__(self):
        super(Filter, self).__init__(__name__)

    def get_results(self, where_string, data):
        ips = service.ipentry.IPEntry()
        return ips.find_all_ips(where_string, data)


# string =  'a' (anything)*:c 'a' -> ''.join(c)
    def parse_dsl(self, lang):
        where = []
        conjunctions = []
        errors = ""

        if len(lang.strip()) == 0:
            return {'where_string': "", 'values': []}

        try:
            def ex(left, op, right):
                e = [left, op, right]
                where.append(e)
                return (left, op, right)
            def q(op, ex):
                # data.append(op)
                return (op, ex)
            def conj(op, ex):
                conjunctions.append(op)
                return (op, ex)

            x = parsley.makeGrammar("""
            string =  '"' (~'"' anything)*:s '"' -> ''.join(s)
            expr = string:left ws ('='|'!='|'>'|'<'):compop ws string:right -> ex(left, compop, right)
            and = 'and' ws query2:n -> conj('and', n)
            or = 'or' ws query2:n -> conj('or', n)
            conj = ws (and | or)
            query2 = expr:e1 conj*:cnj ->  q(cnj, e1)
            query = query2:e1 conj*:cnj -> q(cnj, e1)
            """, {"ex" : ex, "q" : q, "conj" : conj })
            x(lang).query()


            i = 0
            max = len(conjunctions)
            where_string = "where "
            values = []
            for ex in where:
                t1, op, t2 = ex
                # where_string += "lower(" + t1 +  ")"
                where_string += "lower(" + t1 + ")"
                where_string += " " + op + "lower( %s )"
                if t1 == "ip":
                    t2 = int(netaddr.IPAddress(t2))
                values.append(t2)
                if i < max:
                    where_string += conjunctions[i] + " "
                i += 1

            # print where_string
            # print values
            return { 'where_string' : where_string, 'values' : values}
        except Exception, e:
            errors = str(e)
            return {'error': errors }

        # select_ip = ("select ip, city from iplist where ip != %s and city = %s")
        # data_ip = ( ip, "Berlin", )
