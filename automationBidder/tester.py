from rediscluster import RedisCluster

startup_nodes_queue = [{"host": "core-dev.pid24g.clustercfg.usw2.cache.amazonaws.com", "port": 6379}]
rc = RedisCluster(startup_nodes=startup_nodes_queue, decode_responses=True, skip_full_coverage_check=True)

mapping = {
                "width": record['width'] or '',
                "height": record['height'] or '',
                "advertiser_id": record['advertiser_id'] or '',
                "creative_id": record['partner_creative_id'] or '',
                "campaign_id": record['campaign_id'] or '',
                "line_item_id": record['line_item_id'] or '',
                "objective_id": record['objective_id'] or '',
                "channel_id": record['channel_id'] or '',
                "recency_threshold": record['recency_threshold'] or '',
                "household_score_threshold": record['household_score_threshold']  or '',
                "viewability_score_threshold": record['viewability_score_threshold'] or '',
                "pace_multiplier": pace_multiplier,
            }

                key = "crid_" + str(record['partner_creative_id'])

                rc.hmset(name=key, mapping=mapping)