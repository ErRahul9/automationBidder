from rediscluster import RedisCluster
import psycopg2
import os

def connectToCache(host, port, mapping, key,action):
    ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "..","resources"))
    startup_nodes = [{"host": host, "port": port}]
    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)
    getValue = ""
    if "insert" in action:
        if "segment" in host:
            for keys in mapping:
                rc.set(key, mapping.get(keys))
                getValue = rc.get(key)
        elif "member" in host:
            for keys in mapping:
                rc.sadd(keys,mapping.get(keys))
                getValue = rc.smembers(keys)
        else:
            rc.hmset(name=key,mapping=mapping)
            getValue = rc.hgetall(key)
    elif "delete" in action:
        rc.flushall()
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

