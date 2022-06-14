from rediscluster import RedisCluster
import psycopg2


def connectToCache(host, port, keyVal):
    width = 300
    height = 50
    startup_nodes = [{"host": host, "port": port}]
    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)
    key = rc.hgetall(keyVal)
    getValue = str(key.get(str(width) + ":" + str(height) + "_avg_cpi"))
    # print(getValue)
    return getValue


def connectTopostgres(sql, password):
    conn = psycopg2.connect(
        host="integration-dev.crvrygavls2u.us-west-2.rds.amazonaws.com",
        database="qacoredb",
        user="qacore",
        port=5432,
        password=password)
    # password
    cur = conn.cursor()
    cur.execute(sql)
    for rows in cur.fetchall():
        print(rows)


def updateDataInCaches(self):
    print(self.jsonfile)

    # with open(self.bidderfile) as f:
    #     print(f.read())
    # # print("creating bidder file")


def connectToBeeswax():
    '''
    beeswax-api-master/beeswax/tools/bid/bid


    ./bidding_agent_requests_generator bidder_try_5.txt
     http://bidder.coredev.west2.steelhouse.com/beeswax/bidder
     --log-level debug
     --path-to-responses-file ./output.txt && cat output.txt


    '''
    print("connecting to postgres")


# print(connectToCache("core-dev-bidder-price.pid24g.clustercfg.usw2.cache.amazonaws.com", 6379,"com.dailymail.online"))
print(connectTopostgres("select * from public.creative_metadata limit 10", "qa#core07#19"))
