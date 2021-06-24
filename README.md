# pubsub-magician

Helps work with pubsub and pubsub-emulator

## Getting Started
Use the Makefile of python directly.

### Set pubsub emulator variables (only if using pubsub emulator)

```bash
make set-vars
```

### Start pubsub emulator with project-id=my-project (the project doesn't need to exist)

```bash
make start-emulator
```

### Create topic

```bash
make create-topic TOPIC=my-topic
```

### Create subscription

```bash
make create-sub TOPIC=my-topic SUB=my-sub
```

### List topics

```bash
make list-topic
```

### List subscriptions

```bash
make list-sub 
```

### Publish messages

```bash
python publisher.py my-project my-topic --unique --num_msgs=10
```

### Pull messages

```bash
make pull SUB=my-sub TIMEOUT=10
```
