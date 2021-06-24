"""Publishes messages to Pub/Sub topic
"""

import argparse
import json
import random
import time

from google.cloud import pubsub_v1

pubsub_client = pubsub_v1.PublisherClient()


def publish(topic, is_unique_ids):
    random_id = random.randrange(10000000001, 99999999999, 1)
    event_time = time.time()
    # data = {
    #     "idfa": 100000001 if is_unique_ids else random_id,
    #     "event_time": event_time
    # }

    data = {
        "root_element": {
            "event_type": "click",
            "adjustment_status": None,
            "measure": {
                "is_limited_ad_tracking_enabled": 0
            },
            "tracking_metadata": {
                "partner_id": "muv_mobile|MobUpps"
            },
            "user_device": {
                "platform": "iOS",
                "aaid": None,
                "idfa": str(10000000001 if is_unique_ids else random_id),
            }
        }
    }


    payload = json.dumps(data)
    future = pubsub_client.publish(topic, payload.encode("utf-8"),
                                   timestamp=str(round(event_time * 1000)),
                                   message_id=str(random_id))
    print(data)
    print(future.result())
    time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    parser.add_argument("topic_id", help="The topic_id to publish messages")
    parser.add_argument("--num_msgs", type=float, nargs='?', help="Number of messages to be published")
    parser.add_argument("--unique", action='store_true', help="Use unique ids")
    args = parser.parse_args()

    topic_path = pubsub_client.topic_path(args.project_id, args.topic_id)

    num_msgs = 0
    while not args.num_msgs or num_msgs < args.num_msgs:
        publish(topic_path, args.unique)
        num_msgs = num_msgs + 1
