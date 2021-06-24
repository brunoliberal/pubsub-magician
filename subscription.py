"""Manage subscriptions
"""

import argparse
from google.cloud import pubsub_v1

PUBLISHER_CLIENT = pubsub_v1.PublisherClient()
SUBSCRIBER_CLIENT = pubsub_v1.SubscriberClient()


def create_subscription(project_id, topic_id, subscription_id):
    """Create a new pull subscription on the given topic."""
    topic_path = PUBLISHER_CLIENT.topic_path(project_id, topic_id)
    subscription_path = SUBSCRIBER_CLIENT.subscription_path(project_id, subscription_id)

    with SUBSCRIBER_CLIENT:
        subscription = SUBSCRIBER_CLIENT.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )

    print(f"Subscription created: {subscription}")


def delete_subscription(project_id, subscription_id):
    """Deletes an existing Pub/Sub topic."""
    subscription_path = SUBSCRIBER_CLIENT.subscription_path(project_id, subscription_id)

    with SUBSCRIBER_CLIENT:
        SUBSCRIBER_CLIENT.delete_subscription(request={"subscription": subscription_path})
    print(f"Subscription deleted: {subscription_path}.")


def list_subscriptions_in_project(project_id):
    """Lists all subscriptions in the current project."""
    project_path = f"projects/{project_id}"
    with SUBSCRIBER_CLIENT:
        for subscription in SUBSCRIBER_CLIENT.list_subscriptions(
            request={"project": project_path}
        ):
            print(subscription.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help=create_subscription.__doc__)
    create_parser.add_argument("topic_id")
    create_parser.add_argument("subscription_id")

    delete_parser = subparsers.add_parser("delete", help=delete_subscription.__doc__)
    delete_parser.add_argument("subscription_id")

    list_in_project_parser = subparsers.add_parser("list", help=list_subscriptions_in_project.__doc__)

    args = parser.parse_args()
    if args.command == "create":
        create_subscription(args.project_id, args.topic_id, args.subscription_id)
    elif args.command == "delete":
        delete_subscription(args.project_id, args.subscription_id)
    elif args.command == "list":
        list_subscriptions_in_project(args.project_id)
