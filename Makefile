PUBSUB_EMULATOR_HOST=localhost:8085
PUBSUB_PROJECT_ID=my-project

set-vars:
	export PUBSUB_EMULATOR_HOST=$(PUBSUB_EMULATOR_HOST); \
	export PUBSUB_PROJECT_ID=$(PUBSUB_PROJECT_ID)

start-emulator:
	@gcloud beta emulators pubsub start --project=$(PUBSUB_PROJECT_ID)

create-topic:
	@python topic.py $(PUBSUB_PROJECT_ID) create $(TOPIC)

list-topic:
	@python topic.py $(PUBSUB_PROJECT_ID) list

create-sub:
	@python subscription.py $(PUBSUB_PROJECT_ID) create $(TOPIC) $(SUB)

list-sub:
	@python subscription.py $(PUBSUB_PROJECT_ID) list

publish:
	@python publisher.py $(PUBSUB_PROJECT_ID) $(TOPIC) $(NUM_MSGS)

pull:
	@python subscriber.py $(PUBSUB_PROJECT_ID) receive $(SUB) $(TIMEOUT)