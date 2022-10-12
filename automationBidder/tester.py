# import sys
#
# import main
#
#
#
# print(main.main("Augmentor").returnPaths().get("resource"))
# print(main.main("Augmentor").returnPaths().get("resource"))
# print(main.main("Augmentor").returnPaths().get("resource"))
# print(main.main("Augmentor").returnPaths().get("resource"))
#
# # print(sys.path)
# test_array = [1,2,3,a,5,6]


# result = filter(value => type(value) == int, test_array)

# from rediscluster import RedisCluster
# startup_nodes_queue = [{"host": "core-dev-bidder-price-optimize.pid24g.clustercfg.usw2.cache.amazonaws.com", "port": 6379}]
# rc = RedisCluster(startup_nodes=startup_nodes_queue, decode_responses=True, skip_full_coverage_check=True)
# key = "default"
# mapping = { "1920:1080_avg_cpi": 1099}
# rc.sadd(key, mapping)



'''
 mapping = {
                    str(record['width']) + ":" + str(record['height'])+"_avg_cpi": int(record['avg_cpi']),
                    str(record['width']) + ":" + str(record['height'])+"_min_cpi": int(record['min_cpi']),
                    str(record['width']) + ":" + str(record['height'])+"_max_cpi": int(record['max_cpi']),
                    str(record['viewability_rate']): int(record['viewability_rate'])
                }


'''