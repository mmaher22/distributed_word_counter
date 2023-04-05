# Word Count Dashboard

This repository contains an implementation of a word count dashboard that uses a fog computing architecture to compute the most frequently used words from a stream of text data. The system consists of multiple remote nodes that process the stream of data and a central node that aggregates the results and displays them on a dashboard.

### Architecture
The system architecture consists of the following components:

1. **Data Generator**: A Python script that generates a stream of text data and sends it to a Kafka topic.
2. **Remote Node**: A Python script that consumes the text data from a Kafka topic, computes the word count and updates it in a Redis database. It also publishes a copy of the original text message to another Kafka topic for further processing by the central node.
3. **Central Node**: A Python script that subscribes to the Kafka topic that contains the processed text data, aggregates the word counts from each remote node and displays the top 10 most frequently used words on a dashboard.
The system follows the fog computing approach by performing part of the computation on edge nodes (remote nodes) and then aggregating and finalizing the results on a central node.

### Getting Started
To get started with the system, follow these steps:

1. Install Docker and Docker Compose on your machine.
2. Clone this repository to your local machine.
3. Navigate to the repository directory and run the following command to start the system:
```
docker-compose up
```

4. Wait for the system to start up. You can check the logs to monitor the progress.
Once the system is up and running, open a web browser and navigate to http://localhost:8050 to view the dashboard.

### Configuration
The system can be configured using environment variables. The following variables are supported:

* ```KAFKA_SERVER```: The address of the Kafka server. Defaults to localhost:9092.
* ```REDIS_SERVER```: The address of the Redis server. Defaults to localhost.
* ```REDIS_PORT```: The port number of the Redis server. Defaults to 6379.
* ```REDIS_PUBSUB_CHANNEL```: The name of the Redis pub/sub channel for word count updates. Defaults to word_count_updates.
* ```FETCH_INTERVAL```: The interval at which the remote nodes fetch data from Kafka. Defaults to 5 seconds.
* ```DASHBOARD_REFRESH_INTERVAL```: The interval at which the dashboard updates. Defaults to 10 seconds.

### Contributors
Mohamed Maher (m.maher525@gmail.com)