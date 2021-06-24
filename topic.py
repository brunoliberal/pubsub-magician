"""Manage topics
"""

import argparse
from google.cloud import pubsub_v1

PUBLISHER_CLIENT = pubsub_v1.PublisherClient()


def list_topics(project_id):
    """Lists all Pub/Sub topics in the given project."""
    project_path = f"projects/{project_id}"
    for topic in PUBLISHER_CLIENT.list_topics(request={"project": project_path}):
        print(topic)


def create_topic(project_id, topic_id):
    """Create a new Pub/Sub topic."""
    topic_path = PUBLISHER_CLIENT.topic_path(project_id, topic_id)
    topic = PUBLISHER_CLIENT.create_topic(request={"name": topic_path})
    print("Created topic: {}".format(topic.name))


def delete_topic(project_id, topic_id):
    """Deletes an existing Pub/Sub topic."""
    topic_path = PUBLISHER_CLIENT.topic_path(project_id, topic_id)
    PUBLISHER_CLIENT.delete_topic(request={"topic": topic_path})
    print("Topic deleted: {}".format(topic_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help=list_topics.__doc__)

    create_parser = subparsers.add_parser("create", help=create_topic.__doc__)
    create_parser.add_argument("topic_id")

    delete_parser = subparsers.add_parser("delete", help=delete_topic.__doc__)
    delete_parser.add_argument("topic_id")

    args = parser.parse_args()
    if args.command == "list":
        list_topics(args.project_id)
    elif args.command == "create":
        create_topic(args.project_id, args.topic_id)
    elif args.command == "delete":
        delete_topic(args.project_id, args.topic_id)