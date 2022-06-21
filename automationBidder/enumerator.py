import enum


class enumerator(enum.Enum):
    domainId = "domain"
    campaignid = "campaign_id"
    creativeId = ["creative_ids","creative_id"]
    advertiserId = "advertiser_id"
    width = ["w","width"]
    height = ["h","height"]
    lineItemId = "line_item_id"
    objectiveId = "objective_id"
    channelId = "channel_id"
    ip = ["ip_address","ip"]
    paceMultipler = "pace_multiplier"

