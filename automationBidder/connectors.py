import json

from rediscluster import RedisCluster

# import rediscluster


def connectToCache(host,port,keyVal):
    width = 300
    height = 50
    startup_nodes = [{"host": host, "port": port}]
    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)
    key = rc.hgetall(keyVal)
    getValue = str(key.get(str(width)+":"+str(height)+"_avg_cpi"))
    # print(getValue)
    return getValue


def connectTopostgres():
    print("connecting to postgres")


def connectToBeeswax():
    print("connecting to postgres")

'''
w: 300
      h: 600

'''

print(connectToCache("core-dev-bidder-price.pid24g.clustercfg.usw2.cache.amazonaws.com", 6379,"com.dailymail.online"))