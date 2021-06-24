"""Pull subscriptions."""
import argparse
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError


SUBSCRIBER_CLIENT = pubsub_v1.SubscriberClient()


def receive_messages(project_id, subscription_id, timeout=None):
    """Receives messages from a pull subscription."""
    subscription_path = SUBSCRIBER_CLIENT.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received {message}.")
        message.ack()

    streaming_pull_future = SUBSCRIBER_CLIENT.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    with SUBSCRIBER_CLIENT:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")
    subparsers = parser.add_subparsers(dest="command")
    receive_parser = subparsers.add_parser("receive", help=receive_messages.__doc__)
    receive_parser.add_argument("subscription_id")
    receive_parser.add_argument("timeout", default=None, type=float, nargs="?")

    args = parser.parse_args()

    if args.command == "receive":
        receive_messages(args.project_id, args.subscription_id, args.timeout)
